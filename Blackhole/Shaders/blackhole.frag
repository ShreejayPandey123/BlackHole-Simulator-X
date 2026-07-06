#version 330

in vec2 texcoord;
out vec4 fragColor;

uniform vec2 u_resolution;
uniform float u_time;
uniform float u_spin;
uniform float u_cam_r;
uniform float u_cam_th;
uniform float u_cam_ph;
uniform float u_fov;
uniform float u_lensing;
uniform float u_doppler;
uniform float u_redshift;
uniform float u_jets;
uniform float u_jet_power;
uniform float u_disk_r_out;
uniform float u_disk_thickness;
uniform float u_disk_temp;
uniform float u_opt_density;
uniform float u_mass;
uniform int u_quality_steps;

#define PI 3.14159265359
#define R_ESCAPE 60.0

struct State {
    float r;
    float th;
    float ph;
    float pr;
    float pth;
};

float hash21(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

float vnoise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    float a = hash21(i);
    float b = hash21(i + vec2(1.0, 0.0));
    float c = hash21(i + vec2(0.0, 1.0));
    float d = hash21(i + vec2(1.0, 1.0));
    return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}

float fbm(vec2 p) {
    float v = 0.0;
    float amp = 0.5;
    vec2 q = p;
    for (int i = 0; i < 4; i++) {
        v += amp * vnoise(q);
        q = vec2(0.8 * q.x - 0.6 * q.y, 0.6 * q.x + 0.8 * q.y) * 2.03;
        amp *= 0.5;
    }
    return v;
}

float hash31(vec3 p) {
    return fract(sin(dot(p, vec3(17.1, 31.7, 61.3))) * 43758.5453);
}

vec3 sky_color(vec3 d) {
    vec3 col = vec3(0.003, 0.004, 0.008);
    float band = exp(-4.5 * pow(d.y + 0.35 * d.x, 2.0));
    col += vec3(0.025, 0.020, 0.032) * band * (0.4 + 0.6 * fbm(vec2(d.x + 2.0 * d.z, d.y) * 5.0));
    
    vec3 p = d * 48.0;
    vec3 cell = floor(p);
    float rnd = hash31(cell);
    if (rnd > 0.90) {
        vec3 sp = cell + 0.5 + 0.6 * (vec3(hash31(cell + vec3(1.3, 0.0, 0.0)), hash31(cell + vec3(0.0, 2.7, 0.0)), hash31(cell + vec3(0.0, 0.0, 4.1))) - 0.5);
        vec3 sd = normalize(sp);
        float ang = acos(clamp(dot(d, sd), -1.0, 1.0));
        vec3 tint = mix(vec3(0.75, 0.82, 1.0), vec3(1.0, 0.85, 0.7), hash31(cell + vec3(9.9, 0.0, 0.0)));
        col += tint * (rnd - 0.90) * 26.0 * exp(-pow(ang / 0.0035, 2.0));
    }
    return col;
}

vec3 blackbody_rgb(float T) {
    float t = clamp(T, 1000.0, 40000.0) / 100.0;
    float r = 1.0;
    float g = 1.0;
    float b = 1.0;
    
    if (t <= 66.0) {
        g = clamp((99.4708025861 * log(t) - 161.1195681661) / 255.0, 0.0, 1.0);
        b = 0.0;
        if (t > 19.0) {
            b = clamp((138.5177312231 * log(t - 10.0) - 305.0447927307) / 255.0, 0.0, 1.0);
        }
    } else {
        r = clamp(329.698727446 * pow(t - 60.0, -0.1332047592) / 255.0, 0.0, 1.0);
        g = clamp(288.1221695283 * pow(t - 60.0, -0.0755148492) / 255.0, 0.0, 1.0);
    }
    return vec3(r, g, b);
}

State geodesic_rhs(State y, float E, float L, float a) {
    float r = y.r;
    float th = y.th;
    float pr = y.pr;
    float pth = y.pth;
    
    float s = sin(th);
    float c = cos(th);
    if (abs(s) < 1e-5) {
        s = 1e-5 * (s >= 0.0 ? 1.0 : -1.0);
    }
    
    float sigma = r * r + a * a * c * c;
    float delta = r * r - 2.0 * r + a * a;
    float P = E * (r * r + a * a) - a * L;
    float Wt = L / s - a * E * s;
    
    float F = delta * pr * pr + pth * pth - P * P / delta + Wt * Wt;
    float Hc = F / (2.0 * sigma);
    
    float dr = delta * pr / sigma;
    float dth = pth / sigma;
    float dph = (a * P / delta + Wt / s) / sigma;
    
    float ddel = 2.0 * r - 2.0;
    float Fr = ddel * pr * pr - (2.0 * P * (2.0 * E * r) * delta - P * P * ddel) / (delta * delta);
    float Fth = 2.0 * Wt * (-L * c / (s * s) - a * E * c);
    
    float dpr = -(Fr - 2.0 * Hc * (2.0 * r)) / (2.0 * sigma);
    float dpth = -(Fth - 2.0 * Hc * (-2.0 * a * a * s * c)) / (2.0 * sigma);
    
    State dy;
    dy.r = dr;
    dy.th = dth;
    dy.ph = dph;
    dy.pr = dpr;
    dy.pth = dpth;
    return dy;
}

State rk4_step(State y, float h, float E, float L, float a) {
    State k1 = geodesic_rhs(y, E, L, a);
    
    State y2;
    y2.r = y.r + 0.5 * h * k1.r;
    y2.th = y.th + 0.5 * h * k1.th;
    y2.ph = y.ph + 0.5 * h * k1.ph;
    y2.pr = y.pr + 0.5 * h * k1.pr;
    y2.pth = y.pth + 0.5 * h * k1.pth;
    State k2 = geodesic_rhs(y2, E, L, a);
    
    State y3;
    y3.r = y.r + 0.5 * h * k2.r;
    y3.th = y.th + 0.5 * h * k2.th;
    y3.ph = y.ph + 0.5 * h * k2.ph;
    y3.pr = y.pr + 0.5 * h * k2.pr;
    y3.pth = y.pth + 0.5 * h * k2.pth;
    State k3 = geodesic_rhs(y3, E, L, a);
    
    State y4;
    y4.r = y.r + h * k3.r;
    y4.th = y.th + h * k3.th;
    y4.ph = y.ph + h * k3.ph;
    y4.pr = y.pr + h * k3.pr;
    y4.pth = y.pth + h * k3.pth;
    State k4 = geodesic_rhs(y4, E, L, a);
    
    State yn;
    yn.r = y.r + (h / 6.0) * (k1.r + 2.0 * k2.r + 2.0 * k3.r + k4.r);
    yn.th = y.th + (h / 6.0) * (k1.th + 2.0 * k2.th + 2.0 * k3.th + k4.th);
    yn.ph = y.ph + (h / 6.0) * (k1.ph + 2.0 * k2.ph + 2.0 * k3.ph + k4.ph);
    yn.pr = y.pr + (h / 6.0) * (k1.pr + 2.0 * k2.pr + 2.0 * k3.pr + k4.pr);
    yn.pth = y.pth + (h / 6.0) * (k1.pth + 2.0 * k2.pth + 2.0 * k3.pth + k4.pth);
    return yn;
}

void camera_ray(float nr, float nth, float nph, float r, float th, float a, out float E, out float L, out float pr, out float pth) {
    float s = sin(th);
    float c = cos(th);
    if (abs(s) < 1e-5) {
        s = 1e-5 * (s >= 0.0 ? 1.0 : -1.0);
    }
    float sigma = r * r + a * a * c * c;
    float delta = r * r - 2.0 * r + a * a;
    float A2 = pow(r * r + a * a, 2.0) - a * a * delta * s * s;
    float g_tt = -(1.0 - 2.0 * r / sigma);
    float g_tp = -2.0 * a * r * s * s / sigma;
    float g_pp = A2 * s * s / sigma;
    float omega = 2.0 * a * r / A2;
    float alpha = sqrt(delta * sigma / A2);
    
    float pt = 1.0 / alpha;
    float pp = omega / alpha + nph / sqrt(g_pp);
    E = -(g_tt * pt + g_tp * pp);
    L = g_tp * pt + g_pp * pp;
    pr = nr * sqrt(sigma / delta);
    pth = nth * sqrt(sigma);
}

float disk_temperature(float r, float rin) {
    float x = max(r / rin, 1.0001);
    float f = pow(x, -0.75) * pow(1.0 - sqrt(1.0 / x), 0.25);
    return u_disk_temp * f / 0.4879;
}

vec3 shade_disk(float r, float ph, float E, float L, float a, float rin, float t) {
    float om = 1.0 / (pow(r, 1.5) + a);
    float g_tt = -(1.0 - 2.0 / r);
    float g_tp = -2.0 * a / r;
    float g_pp = r * r + a * a + 2.0 * a * a / r;
    float ut2 = -(g_tt + 2.0 * om * g_tp + om * om * g_pp);
    vec3 col = vec3(0.0);
    
    if (ut2 > 1e-6) {
        float ut = 1.0 / sqrt(ut2);
        float gfac = 1.0;
        if (u_doppler > 0.5) {
            gfac = min(1.0 / (ut * (E - om * L)), 4.0);
        }
        float T_em = disk_temperature(r, rin);
        
        vec2 pco = vec2(r * cos(ph - om * t), r * sin(ph - om * t));
        float tex = 0.22 + 1.3 * pow(fbm(pco * 1.3), 2.0);
        
        float intensity = pow(gfac, 4.0) * pow(T_em / u_disk_temp, 4.0) * tex;
        float T_obs = (u_redshift > 0.5) ? (gfac * T_em) : T_em;
        col = blackbody_rgb(T_obs) * intensity * 1.6 * u_opt_density;
    }
    return col;
}

vec3 get_asymptotic_direction(State s, State d) {
    float sth = sin(s.th);
    float cth = cos(s.th);
    float sph = sin(s.ph);
    float cph = cos(s.ph);
    float r1 = s.r;
    
    float dx = d.r * sth * cph + r1 * cth * cph * d.th - r1 * sth * sph * d.ph;
    float dy = d.r * sth * sph + r1 * cth * sph * d.th + r1 * sth * cph * d.ph;
    float dz = d.r * cth - r1 * sth * d.th;
    
    return normalize(vec3(dx, dy, dz));
}

void main() {
    vec2 uv = (gl_FragCoord.xy + 0.5 - 0.5 * u_resolution) / u_resolution.y;
    
    float a = u_spin;
    float rc = u_cam_r;
    float thc = u_cam_th;
    float phc = u_cam_ph;
    float tanf = tan(u_fov * 0.5);
    float r_hor = 1.0 + sqrt(1.0 - a * a);
    
    float z1 = 1.0 + pow(1.0 - a * a, 1.0 / 3.0) * (pow(1.0 + a, 1.0 / 3.0) + pow(1.0 - a, 1.0 / 3.0));
    float z2 = sqrt(3.0 * a * a + z1 * z1);
    float r_isco = 3.0 + z2 - sqrt((3.0 - z1) * (3.0 + z1 + 2.0 * z2));
    
    float rstop = r_hor + 0.02;
    vec3 n = normalize(vec3(-1.0, -tanf * uv.y, tanf * uv.x));
    vec3 col = vec3(0.0);
    
    if (u_lensing < 0.5) {
        // FLAT SPACE (NO LENSING)
        vec3 P_cam = vec3(
            rc * sin(thc) * cos(phc),
            rc * sin(thc) * sin(phc),
            rc * cos(thc)
        );
        
        vec3 er = vec3(sin(thc) * cos(phc), sin(thc) * sin(phc), cos(thc));
        vec3 eth = vec3(cos(thc) * cos(phc), cos(thc) * sin(phc), -sin(thc));
        vec3 eph = vec3(-sin(phc), cos(phc), 0.0);
        
        vec3 v_dir = n.x * er + n.y * eth + n.z * eph;
        
        if (abs(v_dir.z) > 1e-5) {
            float t_int = -P_cam.z / v_dir.z;
            if (t_int > 0.0) {
                vec3 P_int = P_cam + t_int * v_dir;
                float r_int = length(P_int.xy);
                if (r_int >= r_isco && r_int <= u_disk_r_out) {
                    float ph_int = atan(P_int.y, P_int.x);
                    float om = 1.0 / (pow(r_int, 1.5) + a);
                    float ut2 = 1.0 - om * om * r_int * r_int;
                    if (ut2 > 1e-6) {
                        float ut = 1.0 / sqrt(ut2);
                        float cos_flow = -om * r_int * (P_int.x * v_dir.y - P_int.y * v_dir.x) / (r_int * length(v_dir.xy));
                        float gfac = 1.0 / (ut * (1.0 - om * r_int * cos_flow));
                        if (u_doppler < 0.5) gfac = 1.0;
                        
                        float T_em = disk_temperature(r_int, r_isco);
                        vec2 pco = vec2(r_int * cos(ph_int - om * u_time), r_int * sin(ph_int - om * u_time));
                        float tex = 0.22 + 1.3 * pow(fbm(pco * 1.3), 2.0);
                        float intensity = pow(gfac, 4.0) * pow(T_em / u_disk_temp, 4.0) * tex;
                        col = blackbody_rgb(gfac * T_em) * intensity * 1.6 * u_opt_density;
                    }
                } else if (r_int < r_isco) {
                    col = vec3(0.0);
                } else {
                    col = sky_color(v_dir);
                }
            } else {
                col = sky_color(v_dir);
            }
        } else {
            col = sky_color(v_dir);
        }
    } else {
        // GENERAL RELATIVISTIC LENSING
        float E, L, pr0, pth0;
        camera_ray(n.x, n.y, n.z, rc, thc, a, E, L, pr0, pth0);
        
        State y;
        y.r = rc;
        y.th = thc;
        y.ph = phc;
        y.pr = pr0;
        y.pth = pth0;
        
        float jet_opacity_accum = 0.0;
        vec3 jet_color_accum = vec3(0.0);
        
        bool hit_disk = false;
        bool captured = false;
        bool escaped = false;
        State yn;
        
        for (int step = 0; step < u_quality_steps; step++) {
            float hs = 0.16 * clamp(y.r * 0.25, 0.04, 2.2);
            hs *= clamp((y.r - rstop) * 2.0, 0.05, 1.0);
            hs *= clamp(abs(sin(y.th)) * 10.0, 0.05, 1.0);
            
            yn = rk4_step(y, hs, E, L, a);
            
            // Volumetric Jet march
            if (u_jets > 0.5) {
                float rz = y.r * cos(y.th);
                if (abs(rz) > rstop) {
                    float dist_axis = sqrt(y.r * y.r + a * a) * sin(y.th);
                    float jet_r = 0.55 + 0.045 * abs(rz);
                    if (dist_axis < jet_r) {
                        float z_decay = 1.0 / (1.0 + 0.015 * abs(rz));
                        float radial_decay = exp(-3.0 * pow(dist_axis / jet_r, 2.0));
                        float flow_speed = 3.5;
                        vec2 noise_uv = vec2(y.ph * 0.35, abs(rz) * 0.22 - u_time * flow_speed);
                        float noise_factor = 0.45 + 0.9 * fbm(noise_uv);
                        float density = z_decay * radial_decay * noise_factor * u_jet_power * 0.42 * hs;
                        
                        float cos_th = cos(y.th);
                        float sin_th = sin(y.th);
                        float p_r_zamo = y.pr * sqrt((y.r * y.r + a * a * cos_th * cos_th) / (y.r * y.r - 2.0 * y.r + a * a));
                        float p_th_zamo = y.pth * sqrt(y.r * y.r + a * a * cos_th * cos_th);
                        float pz = p_r_zamo * cos_th - p_th_zamo * sin_th;
                        float pz_norm = pz / max(sqrt(p_r_zamo * p_r_zamo + p_th_zamo * p_th_zamo), 1e-5);
                        
                        float cos_flow = (rz >= 0.0 ? 1.0 : -1.0) * pz_norm;
                        float g_jet = 1.0 / (1.4 * (1.0 + 0.7 * cos_flow));
                        float boost = pow(g_jet, 3.0);
                        
                        float u_norm = dist_axis / jet_r;
                        float core_factor = exp(-15.0 * u_norm * u_norm);
                        float sheath_factor = exp(-3.0 * u_norm * u_norm);
                        
                        vec3 base_col = mix(vec3(1.5, 0.2, 2.0), vec3(0.2, 1.0, 2.5), sheath_factor);
                        vec3 jet_col = mix(base_col, vec3(5.0, 5.0, 5.5), core_factor);
                        
                        float jet_opacity = density * boost;
                        
                        jet_color_accum += (1.0 - jet_opacity_accum) * jet_col * jet_opacity * 2.5;
                        jet_opacity_accum += (1.0 - jet_opacity_accum) * jet_opacity;
                    }
                }
            }
            
            // Equatorial plane crossing check
            float c0 = cos(y.th);
            float c1 = cos(yn.th);
            if (c0 * c1 < 0.0) {
                float f = c0 / (c0 - c1);
                float rx = mix(y.r, yn.r, f);
                if (rx >= r_isco && rx <= u_disk_r_out) {
                    float px = mix(y.ph, yn.ph, f);
                    col = shade_disk(rx, px, E, L, a, r_isco, u_time);
                    hit_disk = true;
                    break;
                }
            }
            
            if (yn.r < rstop) {
                captured = true;
                break;
            }
            
            if (yn.r > R_ESCAPE && yn.r > y.r) {
                escaped = true;
                break;
            }
            
            y = yn;
        }
        
        if (hit_disk) {
            if (u_jets > 0.5) {
                col = col * (1.0 - jet_opacity_accum) + jet_color_accum;
            }
        } else if (captured) {
            col = vec3(0.0);
            if (u_jets > 0.5) {
                col = jet_color_accum;
            }
        } else {
            State check_state = escaped ? yn : y;
            State d = geodesic_rhs(check_state, E, L, a);
            vec3 sky_dir = get_asymptotic_direction(check_state, d);
            col = sky_color(sky_dir);
            if (u_jets > 0.5) {
                col = col * (1.0 - jet_opacity_accum) + jet_color_accum;
            }
        }
    }
    
    vec3 c = col;
    vec3 m = c * (2.51 * c + 0.03) / (c * (2.43 * c + 0.59) + 0.14);
    fragColor = vec4(clamp(pow(m, vec3(1.0 / 2.2)), 0.0, 1.0), 1.0);
}