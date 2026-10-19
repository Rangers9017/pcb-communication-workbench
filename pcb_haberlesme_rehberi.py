"""
╔══════════════════════════════════════════════════════════════════════════════╗
║        PCB & HABERLEŞMe REHBERİ — Başlangıç & Orta Düzey                  ║
║   Hesaplama araçları, protokol simülatörleri, mini uygulamalar             ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import math, struct

# ═══════════════════════════════════════════════════════
# RENK PALETİ
# ═══════════════════════════════════════════════════════
BG      = "#1e1e2e"
PANEL   = "#2a2a3e"
PANEL2  = "#313145"
ENTRY   = "#3a3a52"
FG      = "#cdd6f4"
FG2     = "#a6adc8"
FG3     = "#6c7086"
ACCENT  = "#89b4fa"
GREEN   = "#a6e3a1"
RED     = "#f38ba8"
YELLOW  = "#f9e2af"
MAUVE   = "#cba6f7"
TEAL    = "#94e2d5"
PEACH   = "#fab387"

def style_widget(w, **kw):
    try: w.configure(**kw)
    except: pass

# ═══════════════════════════════════════════════════════
# YARDIMCI — scrolled text çıktısı
# ═══════════════════════════════════════════════════════
def make_output(parent, height=10):
    st = scrolledtext.ScrolledText(parent, height=height, bg=ENTRY, fg=GREEN,
                                   font=("Consolas", 9), relief="flat",
                                   insertbackground=FG, wrap="word",
                                   state="normal")
    return st

def out_write(st, text, clear=True):
    st.configure(state="normal")
    if clear: st.delete("1.0", "end")
    st.insert("end", text)
    st.see("end")

def section(text):
    w = 60
    return f"\n{'═'*w}\n  {text}\n{'═'*w}\n"

# ═══════════════════════════════════════════════════════
# LABEL + ENTRY yardımcısı
# ═══════════════════════════════════════════════════════
def lbl_entry(parent, label, default="", row=0, col=0, width=12):
    tk.Label(parent, text=label, bg=PANEL, fg=FG2,
             font=("Segoe UI", 9)).grid(row=row, column=col,
                                        sticky="e", padx=(8,4), pady=4)
    e = tk.Entry(parent, bg=ENTRY, fg=FG, insertbackground=FG,
                 relief="flat", font=("Consolas", 10), width=width)
    e.insert(0, default)
    e.grid(row=row, column=col+1, sticky="w", padx=(0,8), pady=4)
    return e

def calc_btn(parent, text, cmd, row=0, col=0):
    b = tk.Button(parent, text=text, command=cmd,
                  bg=ACCENT, fg=BG, relief="flat",
                  font=("Segoe UI", 9, "bold"), padx=14, pady=5,
                  cursor="hand2", activebackground=MAUVE)
    b.grid(row=row, column=col, columnspan=2, pady=8, padx=8)
    return b

def info_box(parent, text, color=FG2):
    lbl = tk.Label(parent, text=text, bg=PANEL2, fg=color,
                   font=("Segoe UI", 9), justify="left",
                   wraplength=560, padx=10, pady=8, relief="flat")
    lbl.pack(fill="x", padx=8, pady=4)
    return lbl

def title_lbl(parent, text):
    tk.Label(parent, text=text, bg=PANEL, fg=ACCENT,
             font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(10,2))

def sub_lbl(parent, text):
    tk.Label(parent, text=text, bg=PANEL, fg=MAUVE,
             font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=14, pady=(8,2))

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — PCB TEMELLERİ
# ═══════════════════════════════════════════════════════════════════════════════
def build_pcb_tab(nb):
    frame = tk.Frame(nb, bg=PANEL)
    nb.add(frame, text="  PCB Temelleri  ")

    canvas = tk.Canvas(frame, bg=PANEL, highlightthickness=0)
    vsb = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(fill="both", expand=True)
    inner = tk.Frame(canvas, bg=PANEL)
    win_id = canvas.create_window((0,0), window=inner, anchor="nw")
    def on_configure(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(win_id, width=canvas.winfo_width())
    inner.bind("<Configure>", on_configure)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)),"units"))

    title_lbl(inner, "PCB (Printed Circuit Board) — Baskılı Devre Kartı")

    # ── Teori kutuları ──
    theories = [
        ("PCB Nedir?", ACCENT,
         "PCB, elektronik bileşenleri mekanik olarak destekleyen ve elektriksel olarak birbirine\n"
         "bağlayan yalıtkan bir levha üzerinde bakır iletkenler barındıran yapıdır.\n\n"
         "• FR-4: En yaygın malzeme. Epoksi/cam fiber. Tg≈135°C\n"
         "• Alüminyum PCB: LED sürücüler, ısı yönetimi kritik uygulamalar\n"
         "• Flex PCB: Bükülebilir. Giyilebilir elektronik, dar alanlar\n"
         "• Rogers: Yüksek frekans (RF/microwave). 1GHz üzeri"),
        ("PCB Katmanları", MAUVE,
         "Tek Katman (1L): Yalnız bir yüzde bakır. Basit güç devreleri.\n"
         "Çift Katman (2L): Üst (Top) + Alt (Bottom). Çoğu prototip.\n"
         "4 Katman: Top + GND plane + PWR plane + Bottom. Gürültü azalır.\n"
         "6-8+ Katman: Yüksek hızlı dijital, RF, çok katmanlı güç dağıtımı.\n\n"
         "KURAL: Her sinyal katmanının altında/üstünde referans düzlemi (GND/PWR)\n"
         "bulunmalıdır → empedans kontrolü ve EMI azaltımı sağlar."),
        ("Temel Bileşenler", GREEN,
         "SMD (Surface Mount): Yüzeye lehimlenir. 0402, 0603, 0805 boyutlar.\n"
         "THT (Through-Hole): Delikten geçer. Mekanik dayanım yüksek.\n\n"
         "Rezistör  → Akım sınırlama, gerilim bölme, pull-up/pull-down\n"
         "Kondansatör → Bypass (100nF), decoupling, filtre, enerji depolama\n"
         "İndüktör → EMI filtre, DC-DC dönüştürücü (bobin)\n"
         "Diyot → Ters koruma, rectifier, Zener (gerilim referansı)\n"
         "MOSFET/BJT → Anahtarlama, amplifikasyon\n"
         "IC (Entegre) → Mikrodenetleyici, bellek, güç yönetimi"),
        ("Via Tipleri", TEAL,
         "Through-Hole Via: Kartın tamamından geçer. En yaygın.\n"
         "Blind Via: Sadece bir yüzeyden başlar, tüm katmanı geçmez.\n"
         "Buried Via: İç katmanlar arasında. Dışarıdan görünmez.\n"
         "Micro Via (HDI): ≤0.15mm. BGA altı fanout için.\n\n"
         "Via Endüktansı (yaklaşık): L ≈ 0.2·h·[ln(4h/d)+1] nH\n"
         "h=delik uzunluğu(mm), d=çap(mm)\n"
         "→ Yüksek frekanslarda via endüktansı kritik!"),
    ]
    for title, color, txt in theories:
        f = tk.Frame(inner, bg=PANEL2, relief="flat")
        f.pack(fill="x", padx=12, pady=4)
        tk.Label(f, text=f"  ▶ {title}", bg=PANEL2, fg=color,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(6,2), padx=4)
        tk.Label(f, text=txt, bg=PANEL2, fg=FG,
                 font=("Consolas", 9), justify="left", padx=12, pady=6).pack(anchor="w")

    # ── İz Genişliği Hesaplayıcı (IPC-2221) ──
    sub_lbl(inner, "▶ İz (Trace) Genişliği Hesaplayıcı — IPC-2221 Standardı")
    info_box(inner,
             "Formül: W = (I / (k · ΔT^0.44))^(1/0.725) / (T × 1.378)\n"
             "k = 0.048 (iç katman) veya 0.024 (dış katman)\n"
             "ΔT = İzin verilen sıcaklık artışı (°C), T = Bakır kalınlığı (oz → mm: 1oz=0.0347mm)",
             YELLOW)

    fg_pcb = tk.Frame(inner, bg=PANEL); fg_pcb.pack(fill="x", padx=12)
    e_curr  = lbl_entry(fg_pcb, "Akım (A):",       "2.0",  row=0, col=0)
    e_dt    = lbl_entry(fg_pcb, "ΔT maks (°C):",   "10",   row=0, col=2)
    e_oz    = lbl_entry(fg_pcb, "Bakır (oz):",      "1",    row=1, col=0)
    e_layer = lbl_entry(fg_pcb, "Katman (ic/dis):", "dis",  row=1, col=2)
    out_trace = make_output(inner, 8)
    out_trace.pack(fill="x", padx=12, pady=4)

    def calc_trace():
        try:
            I   = float(e_curr.get())
            dT  = float(e_dt.get())
            oz  = float(e_oz.get())
            lay = e_layer.get().strip().lower()
            k   = 0.048 if "dis" in lay else 0.024
            T_mm = oz * 0.0347
            T_mil = T_mm / 0.0254
            # Doğru IPC-2221 formülü:
            # A (cross-section, mils²) = (I / (k*dT^0.44))^(1/0.725)
            # W (mils) = A / T_mils
            A_mils2 = (I / (k * (dT ** 0.44))) ** (1 / 0.725)
            W_mils  = A_mils2 / T_mil
            W_mm    = W_mils * 0.0254
            W_um    = W_mm * 1000

            R_per_cm = (1.724e-6) / (T_mm * 0.1 * W_mm * 0.1)  # Ω/cm (mm→cm)
            R_10cm = R_per_cm * 10
            Pd_10cm = I**2 * R_10cm

            result = f"""
{'─'*52}
  IPC-2221 İz Genişliği Hesabı
{'─'*52}
  Girdi:
    Akım          : {I} A
    ΔT maks       : {dT} °C
    Bakır kalınlığı: {oz} oz = {T_mm:.4f} mm = {T_mil:.2f} mil
    Katman        : {'Dış (Outer)' if 'dis' in lay else 'İç (Inner)'}
    k katsayısı   : {k}

  Hesap:
    Kesit alanı A : {A_mils2:.2f} mils²
    İz genişliği  : {W_mils:.2f} mil
                    {W_mm:.4f} mm
                    {W_um:.1f} µm

  Direnç (20°C):
    Özdirenç Cu   : 1.724×10⁻⁶ Ω·cm
    R (10 cm iz)  : {R_10cm:.4f} Ω  →  P = {Pd_10cm:.4f} W

  Öneri:
    {'✔ Genişlik yeterli (≥0.1mm)' if W_mm >= 0.1 else '⚠ Çok ince! Min. 0.127mm (5mil) tavsiye edilir.'}
    {'⚠ Önemli akım — GND plane bağlantısı ekle!' if I > 5 else ''}
{'─'*52}
"""
            out_write(out_trace, result)
        except Exception as ex:
            out_write(out_trace, f"Hata: {ex}")

    calc_btn(fg_pcb, "İz Genişliğini Hesapla", calc_trace, row=2, col=0)

    # ── Empedans Hesaplayıcı ──
    sub_lbl(inner, "▶ Microstrip Empedans Hesaplayıcı (Z₀)")
    info_box(inner,
             "Microstrip: PCB dış katmanındaki iz (altında referans düzlem var)\n"
             "Z₀ ≈ (87 / √(εr+1.41)) × ln(5.98·h / (0.8·w + t))\n"
             "h=dielektrik kalınlık(mm), w=iz genişliği(mm), t=bakır kalınlık(mm), εr=FR4≈4.4",
             TEAL)

    fg_imp = tk.Frame(inner, bg=PANEL); fg_imp.pack(fill="x", padx=12)
    e_h  = lbl_entry(fg_imp, "h - dielektrik (mm):", "0.2",  row=0, col=0)
    e_w  = lbl_entry(fg_imp, "w - iz genişliği (mm):", "0.35", row=0, col=2)
    e_t  = lbl_entry(fg_imp, "t - bakır kalınlık (mm):", "0.035", row=1, col=0)
    e_er = lbl_entry(fg_imp, "εr (FR4=4.4):", "4.4", row=1, col=2)
    out_imp = make_output(inner, 7)
    out_imp.pack(fill="x", padx=12, pady=4)

    def calc_imp():
        try:
            h  = float(e_h.get())
            w  = float(e_w.get())
            t  = float(e_t.get())
            er = float(e_er.get())
            Z0 = (87 / math.sqrt(er + 1.41)) * math.log(5.98 * h / (0.8 * w + t))
            # Propagation delay (ps/mm)
            td_ps_mm = 3.34 * math.sqrt(0.475 * er + 0.67)
            # Effective εr
            er_eff = ((87 / Z0) * math.sqrt(er + 1.41) / 87) ** 2  # geri hesap
            result = f"""
{'─'*52}
  Microstrip Empedans Hesabı
{'─'*52}
  Girdi:
    Dielektrik kalınlık : h = {h} mm
    İz genişliği        : w = {w} mm
    Bakır kalınlığı     : t = {t} mm ({t/0.0347:.2f} oz)
    Bağıl dielektrik    : εr = {er}

  Sonuç:
    Karakteristik empedans  Z₀ = {Z0:.1f} Ω
    Yayılma gecikmesi       td ≈ {td_ps_mm:.2f} ps/mm

  Hedef empedans karşılaştırma:
    50Ω  (RF/sinyal)    → {'✔ UYGUN' if 48<=Z0<=52 else f'Fark: {Z0-50:+.1f}Ω'}
    100Ω (diferansiyel) → İz çifti: Z_diff ≈ {Z0*1.8:.0f}Ω (yaklaşık)
    75Ω  (video)        → Fark: {Z0-75:+.1f}Ω

  NOT: 50Ω için tipik FR4 (h=1.6mm, 1oz):
    w ≈ 3.0mm (dış katman)
    w ≈ 1.7mm (iç katman, εr etkisi farklı)
{'─'*52}
"""
            out_write(out_imp, result)
        except Exception as ex:
            out_write(out_imp, f"Hata: {ex}")

    calc_btn(fg_imp, "Empedans Hesapla", calc_imp, row=2, col=0)

    return frame


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — GÜÇ & TEMEL HESAPLAMALAR
# ═══════════════════════════════════════════════════════════════════════════════
def build_guc_tab(nb):
    frame = tk.Frame(nb, bg=PANEL)
    nb.add(frame, text="  Güç & Devre  ")

    canvas = tk.Canvas(frame, bg=PANEL, highlightthickness=0)
    vsb = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(fill="both", expand=True)
    inner = tk.Frame(canvas, bg=PANEL)
    win_id = canvas.create_window((0,0), window=inner, anchor="nw")
    def on_conf(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(win_id, width=canvas.winfo_width())
    inner.bind("<Configure>", on_conf)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)),"units"))

    title_lbl(inner, "Temel Devre Hesaplamaları")

    # ── Ohm Kanunu ──
    sub_lbl(inner, "▶ Ohm Kanunu — V = I × R")
    info_box(inner,
             "İki bilinenden üçüncüyü hesapla. Boş bırak = hesaplanacak.\n"
             "V(Volt) = I(Amper) × R(Ohm)    |    P(Watt) = V × I = I²×R = V²/R",
             YELLOW)
    fg_ohm = tk.Frame(inner, bg=PANEL); fg_ohm.pack(fill="x", padx=12)
    e_V = lbl_entry(fg_ohm, "V (Volt):",  "", row=0, col=0)
    e_I = lbl_entry(fg_ohm, "I (Amper):", "", row=0, col=2)
    e_R = lbl_entry(fg_ohm, "R (Ohm):",  "", row=1, col=0)
    out_ohm = make_output(inner, 6)
    out_ohm.pack(fill="x", padx=12, pady=4)

    def calc_ohm():
        V_s = e_V.get().strip(); I_s = e_I.get().strip(); R_s = e_R.get().strip()
        vals = {"V": float(V_s) if V_s else None,
                "I": float(I_s) if I_s else None,
                "R": float(R_s) if R_s else None}
        filled = {k: v for k, v in vals.items() if v is not None}
        if len(filled) < 2:
            out_write(out_ohm, "En az 2 değer girin (üçüncü boş bırakın)."); return
        V, I, R = vals["V"], vals["I"], vals["R"]
        if V is None: V = I * R
        elif I is None: I = V / R
        elif R is None: R = V / I
        P = V * I
        out_write(out_ohm, f"""
{'─'*45}
  Ohm Kanunu Sonuçları
{'─'*45}
  Gerilim  V = {V:.6g} V
  Akım     I = {I:.6g} A  ({I*1000:.4g} mA)
  Direnç   R = {R:.6g} Ω  ({R/1000:.4g} kΩ)
  Güç      P = {P:.6g} W  ({P*1000:.4g} mW)

  Direnç standart değer (E24):
  {e24_nearest(R)}
{'─'*45}
""")

    calc_btn(fg_ohm, "Hesapla", calc_ohm, row=2, col=0)

    # ── Gerilim Bölücü ──
    sub_lbl(inner, "▶ Gerilim Bölücü (Voltage Divider)")
    info_box(inner,
             "Vout = Vin × R2 / (R1 + R2)\n"
             "Kullanım: ADC giriş koruma, referans gerilim, pull-up/down",
             TEAL)
    fg_vd = tk.Frame(inner, bg=PANEL); fg_vd.pack(fill="x", padx=12)
    e_vin  = lbl_entry(fg_vd, "Vin (V):", "12",   row=0, col=0)
    e_r1   = lbl_entry(fg_vd, "R1 (kΩ):", "10",   row=0, col=2)
    e_r2   = lbl_entry(fg_vd, "R2 (kΩ):", "4.7",  row=1, col=0)
    e_rl   = lbl_entry(fg_vd, "Yük RL (kΩ, boş=∞):", "", row=1, col=2)
    out_vd = make_output(inner, 8)
    out_vd.pack(fill="x", padx=12, pady=4)

    def calc_vd():
        try:
            Vin = float(e_vin.get())
            R1  = float(e_r1.get()) * 1000
            R2  = float(e_r2.get()) * 1000
            RL_s = e_rl.get().strip()
            RL  = float(RL_s) * 1000 if RL_s else float("inf")
            R2_eff = R2 if math.isinf(RL) else (R2 * RL) / (R2 + RL)
            Vout   = Vin * R2_eff / (R1 + R2_eff)
            I_total= Vin / (R1 + R2_eff)
            P_R1   = I_total**2 * R1
            P_R2   = (Vout**2) / R2
            loading_err = abs(Vout - Vin*R2/(R1+R2)) / (Vin*R2/(R1+R2)) * 100 if not math.isinf(RL) else 0
            out_write(out_vd, f"""
{'─'*50}
  Gerilim Bölücü Sonuçları
{'─'*50}
  Giriş    Vin  = {Vin:.4g} V
  R1       = {R1/1000:.4g} kΩ  ({R1:.0f} Ω)
  R2       = {R2/1000:.4g} kΩ  ({R2:.0f} Ω)
  {'Yük RL  = ' + f'{RL/1000:.4g} kΩ' if not math.isinf(RL) else 'Yük RL  = ∞ (boşta)'}

  ── Sonuçlar ──
  Vout (yüksüz) = {Vin*R2/(R1+R2):.4g} V
  Vout (yüklü)  = {Vout:.4g} V
  Hata (yükleme)= {loading_err:.2f}%
  I toplam      = {I_total*1000:.4g} mA
  P(R1)         = {P_R1*1000:.4g} mW
  P(R2)         = {P_R2*1000:.4g} mW

  Oran: Vout/Vin = {Vout/Vin:.4f} ({Vout/Vin*100:.2f}%)
{'─'*50}
""")
        except Exception as ex:
            out_write(out_vd, f"Hata: {ex}")

    calc_btn(fg_vd, "Hesapla", calc_vd, row=2, col=0)

    # ── RC Filtre ──
    sub_lbl(inner, "▶ RC Filtre Hesaplayıcı")
    info_box(inner,
             "Alçak Geçiren (Low-pass): Vc = Vin / √(1+(f/fc)²)  |  fc = 1/(2π·R·C)\n"
             "Yüksek Geçiren (High-pass): fc aynı, tepki ters\n"
             "Bypass kondansatör seçimi için de kullanılır.",
             GREEN)
    fg_rc = tk.Frame(inner, bg=PANEL); fg_rc.pack(fill="x", padx=12)
    e_rcR  = lbl_entry(fg_rc, "R (Ω):",          "1000", row=0, col=0)
    e_rcC  = lbl_entry(fg_rc, "C (nF):",          "100",  row=0, col=2)
    e_freq = lbl_entry(fg_rc, "Test frekansı (Hz):", "1000", row=1, col=0)
    out_rc = make_output(inner, 10)
    out_rc.pack(fill="x", padx=12, pady=4)

    def calc_rc():
        try:
            R  = float(e_rcR.get())
            C  = float(e_rcC.get()) * 1e-9
            f  = float(e_freq.get())
            fc = 1 / (2 * math.pi * R * C)
            tau= R * C
            ratio = f / fc
            LP_gain = 1 / math.sqrt(1 + ratio**2)
            HP_gain = ratio / math.sqrt(1 + ratio**2)
            LP_dB = 20 * math.log10(LP_gain)
            HP_dB = 20 * math.log10(HP_gain)
            LP_phase = -math.degrees(math.atan(ratio))
            HP_phase =  math.degrees(math.atan(1/ratio)) if ratio != 0 else 90
            bars = ["▁","▂","▃","▄","▅","▆","▇","█"]
            lp_bar = bars[min(7, int((1-LP_gain)*8))]
            hp_bar = bars[min(7, int(HP_gain*8))]
            out_write(out_rc, f"""
{'─'*55}
  RC Filtre Analizi
{'─'*55}
  R = {R:.4g} Ω,  C = {C*1e9:.4g} nF,  τ = {tau*1000:.4g} ms

  Kesim frekansı fc = {fc:.4g} Hz  ({fc/1000:.4g} kHz)
  (-3dB noktası, %70.7 geçirme)

  Test frekansı f = {f:.4g} Hz  (f/fc = {ratio:.4f})

  ── Alçak Geçiren (Low-Pass) ──
  Kazanç   : {LP_gain:.4f}  ({LP_dB:.2f} dB)
  Faz kayması: {LP_phase:.1f}°
  Zayıflama: {lp_bar} {'GEÇER' if LP_gain > 0.707 else 'ZAYIFLAR' if LP_gain > 0.1 else 'ENGELLENİR'}

  ── Yüksek Geçiren (High-Pass) ──
  Kazanç   : {HP_gain:.4f}  ({HP_dB:.2f} dB)
  Faz kayması: +{HP_phase:.1f}°
  Durum    : {hp_bar} {'GEÇER' if HP_gain > 0.707 else 'ZAYIFLAR' if HP_gain > 0.1 else 'ENGELLENİR'}

  ── Pratik Notlar ──
  Bypass için 100nF seç, fc = {1/(2*math.pi*1000*100e-9):.0f} Hz (R=1kΩ varsayım)
  Dekuplaj: 100nF (VCC pinine yakın) + 10µF (bulk)
{'─'*55}
""")
        except Exception as ex:
            out_write(out_rc, f"Hata: {ex}")

    calc_btn(fg_rc, "RC Analiz Et", calc_rc, row=2, col=0)

    return frame


def e24_nearest(R):
    """E24 serisi en yakın değeri bul."""
    e24 = [1.0,1.1,1.2,1.3,1.5,1.6,1.8,2.0,2.2,2.4,2.7,3.0,
           3.3,3.6,3.9,4.3,4.7,5.1,5.6,6.2,6.8,7.5,8.2,9.1]
    if R <= 0: return "N/A"
    decade = 10 ** math.floor(math.log10(R))
    norm = R / decade
    closest = min(e24, key=lambda x: abs(x - norm))
    val = closest * decade
    if val >= 1e6: return f"{val/1e6:.2g} MΩ"
    if val >= 1e3: return f"{val/1e3:.2g} kΩ"
    return f"{val:.2g} Ω"


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — UART / SERİAL
# ═══════════════════════════════════════════════════════════════════════════════
def build_uart_tab(nb):
    frame = tk.Frame(nb, bg=PANEL)
    nb.add(frame, text="  UART/Serial  ")

    canvas = tk.Canvas(frame, bg=PANEL, highlightthickness=0)
    vsb = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(fill="both", expand=True)
    inner = tk.Frame(canvas, bg=PANEL)
    win_id = canvas.create_window((0,0), window=inner, anchor="nw")
    def on_conf(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(win_id, width=canvas.winfo_width())
    inner.bind("<Configure>", on_conf)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)),"units"))

    title_lbl(inner, "UART — Universal Asynchronous Receiver/Transmitter")

    info_box(inner, """
UART Özellikleri:
  • Asenkron (clock yok), 2 kablo: TX → RX (çapraz bağlantı)
  • Full-duplex: aynı anda iki yönlü iletişim
  • Yaygın baud: 9600, 19200, 38400, 57600, 115200, 921600
  • Her iki taraf aynı baud rate kullanmalı (hata < %2-3 kabul edilir)

Frame Yapısı:
  [BAŞLANGIÇ biti=0] [D0 D1 D2 D3 D4 D5 D6 D7] [PARİTE (ops)] [STOP biti=1]
  ─────────────────────────────────────────────────────────────────
  Boşta hat: LOGİK '1' (HIGH). Başlangıç biti her zaman '0' (LOW).
  STOP biti: '1' (HIGH). 1 veya 2 stop bit kullanılabilir.
""", FG2)

    # Teori kutusu
    theories = [
        ("RS-232 vs RS-485 vs UART TTL", ACCENT,
         "UART TTL (3.3V/5V): Kısa mesafe, kart içi haberleşme. MAX 1m.\n"
         "RS-232: ±3V..±15V. PC COM portu. MAX ~15m, 115200bps'de azalır.\n"
         "RS-485: Diferansiyel (A-B). 1200m mesafe, 10Mbps, multi-drop (32 cihaz).\n"
         "RS-422: RS-485 tek yönlü versiyonu, 4 kablo, full-duplex.\n\n"
         "PCB tasarımı:\n"
         "  RS-232: MAX232 IC (5V↔±12V dönüşüm)\n"
         "  RS-485: MAX485/MAX3485 IC (120Ω terminal direnci gerekli!)"),
        ("Parity Bit Nedir?", GREEN,
         "Veri bütünlüğü kontrolü için eklenen tek bit:\n"
         "  Even (Çift): 1-bitlerin sayısı çift olacak şekilde ayarlanır\n"
         "  Odd  (Tek) : 1-bitlerin sayısı tek olacak şekilde ayarlanır\n"
         "  None: Parity yok (en yaygın: 8N1 = 8 veri, no parity, 1 stop)\n\n"
         "Örnek: 0b01000001 ('A') → 2 tane '1' var\n"
         "  Even parity biti = 0 (zaten çift)\n"
         "  Odd  parity biti = 1 (tek yapmak için)"),
    ]
    for title, color, txt in theories:
        f = tk.Frame(inner, bg=PANEL2, relief="flat")
        f.pack(fill="x", padx=12, pady=3)
        tk.Label(f, text=f"  ▶ {title}", bg=PANEL2, fg=color,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(5,1), padx=4)
        tk.Label(f, text=txt, bg=PANEL2, fg=FG,
                 font=("Consolas", 9), justify="left", padx=12, pady=5).pack(anchor="w")

    # ── Baud Rate Hesaplayıcı ──
    sub_lbl(inner, "▶ Baud Rate & Frame Süresi Hesaplayıcı")
    fg_baud = tk.Frame(inner, bg=PANEL); fg_baud.pack(fill="x", padx=12)
    e_baud  = lbl_entry(fg_baud, "Baud Rate:", "115200", row=0, col=0)
    e_dbits = lbl_entry(fg_baud, "Veri bitleri (7/8):", "8", row=0, col=2)
    e_sbits = lbl_entry(fg_baud, "Stop bitleri (1/2):", "1", row=1, col=0)
    e_parity= lbl_entry(fg_baud, "Parity (0=yok,1=var):", "0", row=1, col=2)
    out_baud = make_output(inner, 10)
    out_baud.pack(fill="x", padx=12, pady=4)

    def calc_baud():
        try:
            baud   = int(e_baud.get())
            dbits  = int(e_dbits.get())
            sbits  = int(e_sbits.get())
            parity = int(e_parity.get())
            total_bits = 1 + dbits + parity + sbits  # start+data+par+stop
            bit_time_us = 1_000_000 / baud
            frame_us    = total_bits * bit_time_us
            frame_ms    = frame_us / 1000
            throughput  = baud * (dbits / total_bits)
            bytes_per_s = throughput / 8
            efficiency  = dbits / total_bits * 100

            std_bauds = [1200,2400,4800,9600,19200,38400,57600,115200,230400,460800,921600]
            nearest = min(std_bauds, key=lambda x: abs(x-baud))
            err_pct = abs(baud - nearest) / nearest * 100

            out_write(out_baud, f"""
{'─'*55}
  UART Baud Rate Analizi
{'─'*55}
  Baud Rate     : {baud} bps
  Frame yapısı  : 1 start + {dbits} data + {parity} parity + {sbits} stop
  Toplam bit/frame: {total_bits} bit

  Zamanlama:
    Bit süresi       : {bit_time_us:.3f} µs
    Frame süresi     : {frame_us:.3f} µs  ({frame_ms:.4f} ms)
    Saniyede frame   : {1_000_000/frame_us:.0f} frame/s

  Verimlilik:
    Net throughput   : {throughput:.0f} bps
    Byte/saniye      : {bytes_per_s:.0f} byte/s  ({bytes_per_s/1024:.2f} KB/s)
    Çerçeve verimliliği: {efficiency:.1f}%

  Standart baud karşılaştırma:
    En yakın standart: {nearest} bps
    Sapma            : {err_pct:.3f}% {'✔ OK' if err_pct < 3 else '⚠ YÜKSEK - sorun çıkabilir!'}

  Örnekler (bu baud ile):
    1KB veri  = {1024/bytes_per_s*1000:.2f} ms
    10KB veri = {10240/bytes_per_s:.3f} s
{'─'*55}
""")
        except Exception as ex:
            out_write(out_baud, f"Hata: {ex}")

    calc_btn(fg_baud, "Baud Analiz Et", calc_baud, row=2, col=0)

    # ── UART Frame Görselleştirici ──
    sub_lbl(inner, "▶ UART Frame Görselleştirici")
    fg_frame = tk.Frame(inner, bg=PANEL); fg_frame.pack(fill="x", padx=12)
    e_uchar  = lbl_entry(fg_frame, "Karakter/HEX (ör: A veya 0x41):", "A", row=0, col=0, width=20)
    e_uparity= lbl_entry(fg_frame, "Parity (none/even/odd):", "none", row=0, col=2, width=10)
    out_uframe = make_output(inner, 10)
    out_uframe.pack(fill="x", padx=12, pady=4)

    def show_frame():
        try:
            raw = e_uchar.get().strip()
            if raw.startswith("0x") or raw.startswith("0X"):
                val = int(raw, 16)
            elif len(raw) == 1:
                val = ord(raw)
            else:
                val = int(raw)
            par_mode = e_uparity.get().strip().lower()
            bits = [(val >> i) & 1 for i in range(8)]
            ones = sum(bits)
            par_bit = None
            if par_mode == "even":
                par_bit = 0 if ones % 2 == 0 else 1
            elif par_mode == "odd":
                par_bit = 1 if ones % 2 == 0 else 0

            frame_bits = [0] + bits  # start + D0..D7
            par_str = ""
            if par_bit is not None:
                frame_bits.append(par_bit)
                par_str = f"{par_bit}"
            frame_bits.append(1)  # stop

            labels = ["START"] + [f"D{i}" for i in range(8)]
            if par_bit is not None: labels.append("PAR")
            labels.append("STOP")

            line1 = " ".join(f"{l:^5}" for l in labels)
            line2 = " ".join(f"{'█'if b else '░':^5}" for b in frame_bits)
            line3 = " ".join(f"{b:^5}" for b in frame_bits)

            out_write(out_uframe, f"""
  Karakter : '{chr(val) if 32<=val<127 else '?'}' (ASCII={val}, HEX=0x{val:02X}, BIN={val:08b})
  Parity   : {par_mode} {'(parity bit=' + par_str + ')' if par_bit is not None else '(yok)'}

  UART Frame (LSB önce gider):
  {line1}
  {line2}
  {line3}

  Dalga şekli (LOW=0, HIGH=1):
  ┐  {"".join('┐' if b else '└' for b in frame_bits)}
  │  {" " * 2}
  └{"─" * (len(frame_bits)*2)}

  Bit gönderim sırası: START=0, D0 (LSB)...D7 (MSB){', PAR' if par_bit is not None else ''}, STOP=1
""")
        except Exception as ex:
            out_write(out_uframe, f"Hata: {ex}")

    calc_btn(fg_frame, "Frame Göster", show_frame, row=1, col=0)

    return frame


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — I2C
# ═══════════════════════════════════════════════════════════════════════════════
def build_i2c_tab(nb):
    frame = tk.Frame(nb, bg=PANEL)
    nb.add(frame, text="  I2C  ")

    canvas = tk.Canvas(frame, bg=PANEL, highlightthickness=0)
    vsb = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(fill="both", expand=True)
    inner = tk.Frame(canvas, bg=PANEL)
    win_id = canvas.create_window((0,0), window=inner, anchor="nw")
    def on_conf(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(win_id, width=canvas.winfo_width())
    inner.bind("<Configure>", on_conf)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)),"units"))

    title_lbl(inner, "I²C — Inter-Integrated Circuit")

    info_box(inner, """
I2C Özellikleri:
  • 2 kablo: SCL (clock) + SDA (data)  — her ikisi de open-drain (pull-up gerekli!)
  • Master/Slave mimarisi. Çok sayıda slave, tek bus.
  • 7-bit adres = 128 adres (16 rezerve → 112 kullanılabilir)
  • 10-bit adres = 1024 adres (gelişmiş mode)
  • Hız: Standard=100kHz, Fast=400kHz, Fast+=1MHz, High-Speed=3.4MHz

Adres Yapısı:
  [7-bit adres | R/W biti] → R=1 (okuma), W=0 (yazma)
  ACK/NACK: Slave her byte sonrası SDA=0 (ACK) veya SDA=1 (NACK) gönderir.
""", FG2)

    theories = [
        ("Pull-up Direnç Seçimi (Kritik!)", RED,
         "I2C open-drain: hat normalde HIGH, cihazlar LOW çeker.\n"
         "Pull-up çok düşük → aşırı akım, güç kaybı\n"
         "Pull-up çok yüksek → kenar yavaşlar, iletişim hatalı\n\n"
         "Formül: Rp_min = (VCC - VOL_max) / IOL_max\n"
         "         Rp_max = tr / (0.8473 × Cb)\n"
         "tr = yükselme süresi, Cb = bus kapasitansı\n\n"
         "Standart (100kHz): 4.7kΩ (3.3V), 10kΩ (5V, kısa bus)\n"
         "Fast (400kHz)    : 1.5kΩ - 2.2kΩ\n"
         "Fast+ (1MHz)     : 1kΩ"),
        ("I2C Yaygın Cihaz Adresleri", TEAL,
         "0x48-0x4F : LM75, TMP102 (sıcaklık sensörü)\n"
         "0x68-0x6F : MPU-6050, DS1307 (IMU, RTC)\n"
         "0x3C, 0x3D: SSD1306 (OLED ekran)\n"
         "0x27, 0x3F: PCF8574 (I/O expander, LCD)\n"
         "0x50-0x57 : AT24C series (EEPROM)\n"
         "0x76,0x77 : BME280, BMP280 (basınç/nem)\n"
         "0x60       : Si5351 (clock generator)\n\n"
         "A0/A1/A2 pinleri ile adres seçimi yapılır → aynı türden 8 cihaz!"),
    ]
    for title, color, txt in theories:
        f = tk.Frame(inner, bg=PANEL2, relief="flat")
        f.pack(fill="x", padx=12, pady=3)
        tk.Label(f, text=f"  ▶ {title}", bg=PANEL2, fg=color,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(5,1), padx=4)
        tk.Label(f, text=txt, bg=PANEL2, fg=FG,
                 font=("Consolas", 9), justify="left", padx=12, pady=5).pack(anchor="w")

    # ── Pull-up Hesaplayıcı ──
    sub_lbl(inner, "▶ I2C Pull-up Direnç Hesaplayıcı")
    fg_i2c = tk.Frame(inner, bg=PANEL); fg_i2c.pack(fill="x", padx=12)
    e_vcc   = lbl_entry(fg_i2c, "VCC (V):",            "3.3",  row=0, col=0)
    e_cb    = lbl_entry(fg_i2c, "Bus kapasitansı (pF):","100",  row=0, col=2)
    e_speed = lbl_entry(fg_i2c, "Hız (kHz):",          "400",  row=1, col=0)
    e_iol   = lbl_entry(fg_i2c, "IOL_max (mA):",        "3",    row=1, col=2)
    out_i2c = make_output(inner, 12)
    out_i2c.pack(fill="x", padx=12, pady=4)

    def calc_pullup():
        try:
            VCC   = float(e_vcc.get())
            Cb    = float(e_cb.get()) * 1e-12
            speed = float(e_speed.get()) * 1000
            IOL   = float(e_iol.get()) * 1e-3
            VOL   = 0.4  # max output low voltage (I2C spec)
            # tr hedefi (I2C spec): 300ns (std), 300ns (fast), 120ns (fast+)
            if speed <= 100e3:   tr = 1000e-9
            elif speed <= 400e3: tr = 300e-9
            else:                tr = 120e-9
            Rp_min = (VCC - VOL) / IOL
            Rp_max = tr / (0.8473 * Cb)
            Rp_opt = (Rp_min + Rp_max) / 2

            modes = {100e3:"Standard (100kHz)", 400e3:"Fast (400kHz)",
                     1e6:"Fast+ (1MHz)", 3.4e6:"High-Speed (3.4MHz)"}
            mode_str = modes.get(speed, f"{speed/1000:.0f}kHz")
            out_write(out_i2c, f"""
{'─'*55}
  I2C Pull-up Direnç Hesabı
{'─'*55}
  VCC    = {VCC} V
  Cb     = {Cb*1e12:.0f} pF  (bus kapasitansı)
  Hız    = {speed/1000:.0f} kHz  ({mode_str})
  IOL    = {IOL*1000:.1f} mA  (max çıkış akımı)
  VOL    = {VOL} V  (max LOW gerilim)

  Hesap:
    Yükselme süresi tr_hedef = {tr*1e9:.0f} ns

    Rp_min = (VCC - VOL) / IOL
           = ({VCC} - {VOL}) / {IOL*1000:.1f}mA = {Rp_min:.0f} Ω  ({Rp_min/1000:.2f} kΩ)

    Rp_max = tr / (0.8473 × Cb)
           = {tr*1e9:.0f}ns / (0.8473 × {Cb*1e12:.0f}pF) = {Rp_max:.0f} Ω  ({Rp_max/1000:.2f} kΩ)

    Optimal Rp ≈ {Rp_opt:.0f} Ω  ({Rp_opt/1000:.2f} kΩ)

  Öneri: {e24_nearest(Rp_opt)}  (E24 standart değer)

  {'✔ Geçerli aralık: ' + f'{Rp_min/1000:.1f}kΩ - {Rp_max/1000:.1f}kΩ' if Rp_min < Rp_max else '⚠ Cb çok yüksek veya hız çok yüksek! Bus kapasitansını azalt.'}

  Akım tüketimi (boşta, HIGH):
    I_pullup = VCC / Rp_opt = {VCC/Rp_opt*1000:.2f} mA (her hat için)
    2 hat toplam = {2*VCC/Rp_opt*1000:.2f} mA
{'─'*55}
""")
        except Exception as ex:
            out_write(out_i2c, f"Hata: {ex}")

    calc_btn(fg_i2c, "Pull-up Hesapla", calc_pullup, row=2, col=0)

    # ── I2C Frame Simülatörü ──
    sub_lbl(inner, "▶ I2C Frame Simülatörü")
    fg_i2cf = tk.Frame(inner, bg=PANEL); fg_i2cf.pack(fill="x", padx=12)
    e_addr7 = lbl_entry(fg_i2cf, "7-bit Adres (hex, ör: 0x48):", "0x48", row=0, col=0, width=12)
    e_rw    = lbl_entry(fg_i2cf, "İşlem (R/W):", "W", row=0, col=2, width=6)
    e_data  = lbl_entry(fg_i2cf, "Veri byte'ları (hex, boşluklu):", "0x12 0x34", row=1, col=0, width=24)
    out_i2cf = make_output(inner, 12)
    out_i2cf.pack(fill="x", padx=12, pady=4)

    def sim_i2c():
        try:
            addr_str = e_addr7.get().strip()
            addr7 = int(addr_str, 16) if addr_str.startswith("0x") else int(addr_str)
            rw = 0 if e_rw.get().strip().upper() == "W" else 1
            addr_byte = (addr7 << 1) | rw
            data_strs = e_data.get().strip().split()
            data_bytes = [int(d, 16) if d.startswith("0x") else int(d) for d in data_strs]
            lines = []
            lines.append(f"{'─'*62}")
            lines.append(f"  I2C Frame Simülasyonu")
            lines.append(f"{'─'*62}")
            lines.append(f"  7-bit Adres  : 0x{addr7:02X} = {addr7:07b}b")
            lines.append(f"  R/W biti     : {rw} ({'OKUMA' if rw else 'YAZMA'})")
            lines.append(f"  Adres byte   : 0x{addr_byte:02X} = {addr_byte:08b}b")
            lines.append("")
            lines.append("  Bus Sekansı:")
            lines.append("  ┌─────────────────────────────────────────────")
            lines.append(f"  │ START → [ADDR=0x{addr_byte:02X} ({addr7:07b}|{rw})] [ACK]")
            for i, db in enumerate(data_bytes):
                lines.append(f"  │ → DATA[{i}] = 0x{db:02X} = {db:08b}b = {db:3d}  [ACK]")
            lines.append(f"  │ STOP")
            lines.append("  └─────────────────────────────────────────────")
            lines.append("")
            lines.append("  SDA/SCL dalga şekli (soyut):")
            lines.append("  SCL: ─┐┌┐┌┐┌┐┌┐┌┐┌┐┌┐┌┐ ... (9 clk/byte: 8 data + 1 ACK)")
            lines.append("  SDA: S─[A6 A5 A4 A3 A2 A1 A0 R/W ACK][D7..D0 ACK]─P")
            lines.append("       ↑ START                                        ↑ STOP")
            out_write(out_i2cf, "\n".join(lines))
        except Exception as ex:
            out_write(out_i2cf, f"Hata: {ex}")

    calc_btn(fg_i2cf, "Frame Simüle Et", sim_i2c, row=2, col=0)

    return frame


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — SPI
# ═══════════════════════════════════════════════════════════════════════════════
def build_spi_tab(nb):
    frame = tk.Frame(nb, bg=PANEL)
    nb.add(frame, text="  SPI  ")

    canvas = tk.Canvas(frame, bg=PANEL, highlightthickness=0)
    vsb = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(fill="both", expand=True)
    inner = tk.Frame(canvas, bg=PANEL)
    win_id = canvas.create_window((0,0), window=inner, anchor="nw")
    def on_conf(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(win_id, width=canvas.winfo_width())
    inner.bind("<Configure>", on_conf)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)),"units"))

    title_lbl(inner, "SPI — Serial Peripheral Interface")

    info_box(inner, """
SPI Özellikleri:
  • 4 kablo: SCK (clock), MOSI (Master Out Slave In),
             MISO (Master In Slave Out), CS/SS (Chip Select, aktif LOW)
  • Senkron, tam çift yönlü (full-duplex)
  • Her slave için ayrı CS hattı gerekir
  • Hız: 1MHz - 100MHz+ (I2C'den çok daha hızlı)
  • Adres yok → CS ile cihaz seçilir

I2C ile Karşılaştırma:
  I2C : Az kablo (+), yavaş (-), ACK/NACK (+), pull-up zorunlu (-)
  SPI : Hızlı (+), çok kablo (-), basit protokol (+), CS/slave başı (-)
""", FG2)

    # SPI Mod tablosu
    sub_lbl(inner, "▶ SPI Modları (CPOL / CPHA)")
    f_modes = tk.Frame(inner, bg=PANEL2)
    f_modes.pack(fill="x", padx=12, pady=4)
    headers = ["Mod", "CPOL", "CPHA", "Clock boşta", "Örnekleme kenarı", "Yaygın Kullanım"]
    rows = [
        ["0", "0", "0", "LOW",  "Rising (↑)",  "SD kart, max7219, bazı ADC"],
        ["1", "0", "1", "LOW",  "Falling (↓)", "Bazı sensörler"],
        ["2", "1", "0", "HIGH", "Falling (↓)", "Bazı DAC, özel IC"],
        ["3", "1", "1", "HIGH", "Rising (↑)",  "MCP2515 (CAN), bazı sensörler"],
    ]
    col_colors = [ACCENT, FG, FG, YELLOW, GREEN, MAUVE]
    for ci, h in enumerate(headers):
        tk.Label(f_modes, text=h, bg=PANEL2, fg=col_colors[ci],
                 font=("Segoe UI", 9, "bold"), padx=8, pady=4,
                 relief="flat").grid(row=0, column=ci, sticky="ew")
    for ri, row in enumerate(rows):
        bg = PANEL if ri % 2 == 0 else PANEL2
        for ci, val in enumerate(row):
            tk.Label(f_modes, text=val, bg=bg, fg=FG,
                     font=("Consolas", 9), padx=8, pady=3).grid(row=ri+1, column=ci, sticky="ew")

    # ── SPI Frame Simülatörü ──
    sub_lbl(inner, "▶ SPI Frame Simülatörü")
    fg_spi = tk.Frame(inner, bg=PANEL); fg_spi.pack(fill="x", padx=12)
    e_spi_data = lbl_entry(fg_spi, "Gönderilecek byte'lar (hex):", "0xAB 0xCD", row=0, col=0, width=24)
    e_spi_mode = lbl_entry(fg_spi, "SPI Modu (0-3):", "0", row=0, col=2, width=4)
    e_spi_bits = lbl_entry(fg_spi, "MSB/LSB first:", "MSB", row=1, col=0, width=6)
    out_spi = make_output(inner, 14)
    out_spi.pack(fill="x", padx=12, pady=4)

    def sim_spi():
        try:
            data_strs = e_spi_data.get().strip().split()
            data = [int(d, 16) if d.startswith("0x") else int(d) for d in data_strs]
            mode = int(e_spi_mode.get().strip())
            msb_first = e_spi_bits.get().strip().upper() != "LSB"
            cpol = (mode >> 1) & 1
            cpha = mode & 1
            lines = []
            lines.append(f"{'─'*62}")
            lines.append(f"  SPI Frame — Mod {mode} (CPOL={cpol}, CPHA={cpha})")
            lines.append(f"{'─'*62}")
            lines.append(f"  Clock boşta : {'HIGH (1)' if cpol else 'LOW (0)'}")
            lines.append(f"  Örnekleme   : {'1.kenar (Rising→Falling)' if not cpha else '2.kenar (Falling→Rising)'} {'(MOSI Rising↑)' if not cpol^cpha else '(MOSI Falling↓)'}")
            lines.append(f"  Bit sırası  : {'MSB' if msb_first else 'LSB'} önce")
            lines.append("")
            lines.append(f"  CS:   ─┐{'─' * (len(data)*12 + 2)}┌─  (LOW=aktif)")
            lines.append(f"  SCK:  ─┘{'└┐'*8*len(data)}└─")
            lines.append("")
            for i, byte in enumerate(data):
                bits = [(byte >> (7-b)) if msb_first else (byte >> b) & 1 for b in range(8)]
                bits_str = " ".join(str(b) for b in bits)
                lines.append(f"  Byte[{i}]: 0x{byte:02X} = {byte:08b}b = {byte:3d}")
                lines.append(f"    MOSI bits: {bits_str}")
                lines.append(f"    MISO bits: (slave cevabı — cihaza göre değişir)")
                lines.append("")
            lines.append("  Toplam CLK darbesi: " + str(len(data) * 8))
            lines.append(f"{'─'*62}")
            out_write(out_spi, "\n".join(lines))
        except Exception as ex:
            out_write(out_spi, f"Hata: {ex}")

    calc_btn(fg_spi, "SPI Frame Simüle Et", sim_spi, row=2, col=0)

    return frame


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 6 — CAN BUS
# ═══════════════════════════════════════════════════════════════════════════════
def build_can_tab(nb):
    frame = tk.Frame(nb, bg=PANEL)
    nb.add(frame, text="  CAN Bus  ")

    canvas = tk.Canvas(frame, bg=PANEL, highlightthickness=0)
    vsb = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(fill="both", expand=True)
    inner = tk.Frame(canvas, bg=PANEL)
    win_id = canvas.create_window((0,0), window=inner, anchor="nw")
    def on_conf(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(win_id, width=canvas.winfo_width())
    inner.bind("<Configure>", on_conf)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)),"units"))

    title_lbl(inner, "CAN Bus — Controller Area Network")

    info_box(inner, """
CAN Bus Özellikleri:
  • ISO 11898 standardı. Otomotiv, endüstri otomasyonu.
  • 2 kablo: CAN_H + CAN_L (diferansiyel)  — 120Ω terminal direnci gerekli!
  • Multi-master: Her node mesaj gönderebilir, arbitrasyon otomatik
  • Hız: 1Mbps (1m), 125kbps (500m), 10kbps (6km)
  • 11-bit (Standard) veya 29-bit (Extended) ID
  • 8 byte veri + CRC + hata algılama (çok güçlü!)

Diferansiyel Sinyal:
  Dominant (0): CAN_H > CAN_L  (CANH≈3.5V, CANL≈1.5V, fark≈2V)
  Recessive (1): CAN_H = CAN_L (her ikisi ≈2.5V, fark≈0V)
  → Gürültüye karşı çok dayanıklı!
""", FG2)

    theories = [
        ("CAN Frame Yapısı", ACCENT,
         "Standard Frame (11-bit ID):\n"
         "  SOF(1) | ID(11) | RTR(1) | IDE(1) | r0(1) | DLC(4) | Data(0-64bit) | CRC(15) | CRC_DEL(1) | ACK(1) | ACK_DEL(1) | EOF(7)\n\n"
         "SOF   : Start Of Frame — dominant bit\n"
         "ID    : Mesaj kimliği (öncelik belirler! DÜŞÜK ID = YÜKSEK ÖNCELİK)\n"
         "RTR   : Remote Transmission Request (0=data, 1=remote frame)\n"
         "IDE   : Identifier Extension (0=standard, 1=extended 29-bit)\n"
         "DLC   : Data Length Code (0-8 byte)\n"
         "CRC   : 15-bit hata kontrol\n"
         "ACK   : Başarılı alımda tüm alıcılar dominant gönderir"),
        ("Bit Timing & Arbitrasyon", GREEN,
         "Bit zamanlaması = 1 / baud_rate\n"
         "Her bit: Sync_Seg + Prop_Seg + Phase_Seg1 + Phase_Seg2\n"
         "Nominal Sample Point genellikle bit zamanının %75-87.5'inde\n\n"
         "Arbitrasyon (CSMA/CA):\n"
         "  Birden fazla node aynı anda gönderirse:\n"
         "  → Her node kendi gönderdiğini okur\n"
         "  → Recessive gönderip Dominant okursa: KAYBETTİ, susturulur\n"
         "  → En düşük ID = Kazanan (en yüksek öncelik)\n"
         "  → ÇARPIŞMA YOK! Sadece öncelik belirlenir."),
        ("Hata Yönetimi", RED,
         "CAN'ın en güçlü özelliklerinden biri hata algılamadır:\n"
         "  Bit Error     : Gönderilen ≠ okunan\n"
         "  Stuff Error   : 5 ardışık aynı bitten sonra ters bit gelmediyse\n"
         "  CRC Error     : Hesaplanan CRC ≠ alınan CRC\n"
         "  Form Error    : Sabit bit alanı ihlali\n"
         "  ACK Error     : Kimse ACK vermedi\n\n"
         "Error Counter: TX_ERR, RX_ERR sayaçları\n"
         "  Error Active  : < 96  (normal)\n"
         "  Error Passive : 96-127 (daha az agresif)\n"
         "  Bus-Off       : > 255  (bus'tan ayrılır, korumalı)"),
    ]
    for title, color, txt in theories:
        f = tk.Frame(inner, bg=PANEL2)
        f.pack(fill="x", padx=12, pady=3)
        tk.Label(f, text=f"  ▶ {title}", bg=PANEL2, fg=color,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(5,1), padx=4)
        tk.Label(f, text=txt, bg=PANEL2, fg=FG,
                 font=("Consolas", 9), justify="left", padx=12, pady=5).pack(anchor="w")

    # ── CAN Bit Timing Hesaplayıcı ──
    sub_lbl(inner, "▶ CAN Bit Timing Hesaplayıcı")
    fg_can = tk.Frame(inner, bg=PANEL); fg_can.pack(fill="x", padx=12)
    e_fosc   = lbl_entry(fg_can, "Osilatör frekansı (MHz):", "16", row=0, col=0)
    e_can_br = lbl_entry(fg_can, "Hedef baud rate (kbps):",  "500", row=0, col=2)
    out_can = make_output(inner, 14)
    out_can.pack(fill="x", padx=12, pady=4)

    def calc_can_timing():
        try:
            fosc = float(e_fosc.get()) * 1e6
            baud = float(e_can_br.get()) * 1e3
            tq = 1 / baud / 10  # yaklaşık, 10 TQ varsayımı
            best = None
            best_err = float("inf")
            for prescaler in range(1, 129):
                tq_actual = prescaler / fosc
                total_tq = round(1 / baud / tq_actual)
                if total_tq < 8 or total_tq > 25:
                    continue
                actual_baud = 1 / (total_tq * tq_actual)
                err = abs(actual_baud - baud) / baud * 100
                if err < best_err:
                    best_err = err
                    best = (prescaler, total_tq, tq_actual, actual_baud)
            if not best:
                out_write(out_can, "Uygun timing bulunamadı. Frekansı/baud'u kontrol edin."); return
            prescaler, total_tq, tq_actual, actual_baud = best
            sp = 75  # %75 sample point
            tseg1 = round(total_tq * sp / 100) - 1
            tseg2 = total_tq - 1 - tseg1
            sjw = min(4, tseg2)
            distances = {125:1000, 250:500, 500:100, 1000:10}
            max_dist = distances.get(int(actual_baud/1000), "?")
            out_write(out_can, f"""
{'─'*58}
  CAN Bit Timing Hesabı
{'─'*58}
  Osilatör  : {fosc/1e6:.0f} MHz
  Hedef baud: {baud/1000:.0f} kbps

  En iyi çözüm:
    BRP (Prescaler) = {prescaler}
    TQ süresi       = {tq_actual*1e9:.3f} ns
    Toplam TQ       = {total_tq} TQ/bit

    TSEG1 (Prop+Phase1) = {tseg1} TQ
    TSEG2 (Phase2)      = {tseg2} TQ
    SJW                 = {sjw} TQ
    Sample Point        = {(tseg1+1)/total_tq*100:.1f}%

  Gerçek baud : {actual_baud/1000:.3f} kbps
  Hata        : {best_err:.4f}% {'✔ KABUL EDİLEBİLİR (<1%)' if best_err < 1 else '⚠ Yüksek hata!'}

  Mesafe tablosu (100pF/m kablo):
    1 Mbps  → max ~40m
    500kbps → max ~100m
    250kbps → max ~250m
    125kbps → max ~500m
    10kbps  → max ~5000m (6km)

  Not: {fosc/1e6:.0f}MHz osilatör için
    MCP2515 (SPI-CAN): BTR1=0x{((tseg2-1)<<4|(tseg1-1)):02X}, BTR2=...
{'─'*58}
""")
        except Exception as ex:
            out_write(out_can, f"Hata: {ex}")

    calc_btn(fg_can, "Bit Timing Hesapla", calc_can_timing, row=1, col=0)

    return frame


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 7 — MODBUS RTU
# ═══════════════════════════════════════════════════════════════════════════════
def build_modbus_tab(nb):
    frame = tk.Frame(nb, bg=PANEL)
    nb.add(frame, text="  Modbus RTU  ")

    canvas = tk.Canvas(frame, bg=PANEL, highlightthickness=0)
    vsb = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(fill="both", expand=True)
    inner = tk.Frame(canvas, bg=PANEL)
    win_id = canvas.create_window((0,0), window=inner, anchor="nw")
    def on_conf(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(win_id, width=canvas.winfo_width())
    inner.bind("<Configure>", on_conf)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)),"units"))

    title_lbl(inner, "Modbus RTU — RS-485 Üzerinde Endüstriyel Haberleşme")

    info_box(inner, """
Modbus RTU Özellikleri:
  • Master/Slave (Client/Server). 1 master, 247 slave (adres 1-247).
  • RS-485 fiziksel katman (diferansiyel, 1200m, gürültüye dayanıklı)
  • Binary format (ASCII versiyonu da var ama daha az yaygın)
  • Frame arası boşluk: 3.5 karakter süresi (sessizlik ile belirlenir)
  • CRC-16 hata kontrolü (Polynomial: 0x8005)

Frame Yapısı:
  [Slave Adres 1B] [Fonksiyon Kodu 1B] [Veri N byte] [CRC 2B (Lo+Hi)]
""", FG2)

    fc_info = tk.Frame(inner, bg=PANEL2)
    fc_info.pack(fill="x", padx=12, pady=4)
    tk.Label(fc_info, text="  ▶ Modbus Fonksiyon Kodları", bg=PANEL2, fg=ACCENT,
             font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(5,2), padx=4)
    fcs = [
        ("FC01 (0x01)", "Read Coils",              "Dijital çıkış okuma (0/1)"),
        ("FC02 (0x02)", "Read Discrete Inputs",    "Dijital giriş okuma (salt okunur)"),
        ("FC03 (0x03)", "Read Holding Registers",  "16-bit okuma/yazma register (en yaygın)"),
        ("FC04 (0x04)", "Read Input Registers",    "16-bit salt okunur register"),
        ("FC05 (0x05)", "Write Single Coil",       "Tek coil yaz (0x0000=OFF, 0xFF00=ON)"),
        ("FC06 (0x06)", "Write Single Register",   "Tek holding register yaz"),
        ("FC15 (0x0F)", "Write Multiple Coils",    "Çoklu coil yaz"),
        ("FC16 (0x10)", "Write Multiple Registers","Çoklu holding register yaz"),
    ]
    for fc, name, desc in fcs:
        row = tk.Frame(fc_info, bg=PANEL2)
        row.pack(fill="x", padx=8, pady=1)
        tk.Label(row, text=fc, bg=PANEL2, fg=YELLOW, font=("Consolas", 9), width=12, anchor="w").pack(side="left")
        tk.Label(row, text=name, bg=PANEL2, fg=PEACH, font=("Consolas", 9), width=26, anchor="w").pack(side="left")
        tk.Label(row, text=desc, bg=PANEL2, fg=FG2, font=("Segoe UI", 9), anchor="w").pack(side="left")

    # ── CRC-16 Hesaplayıcı ──
    sub_lbl(inner, "▶ Modbus CRC-16 Hesaplayıcı")
    info_box(inner, "Polynomial: 0x8005 (reversed: 0xA001). Initial value: 0xFFFF\nAlgoritma: Her byte için 8 bit XOR + shift işlemi.", TEAL)
    fg_crc = tk.Frame(inner, bg=PANEL); fg_crc.pack(fill="x", padx=12)
    e_crc_data = lbl_entry(fg_crc, "Hex data (boşluklu, ör: 01 03 00 00 00 0A):", "01 03 00 00 00 0A", row=0, col=0, width=30)
    out_crc = make_output(inner, 8)
    out_crc.pack(fill="x", padx=12, pady=4)

    def calc_crc16():
        try:
            parts = e_crc_data.get().strip().split()
            data = bytes([int(p, 16) for p in parts])
            crc = 0xFFFF
            for byte in data:
                crc ^= byte
                for _ in range(8):
                    if crc & 0x0001:
                        crc = (crc >> 1) ^ 0xA001
                    else:
                        crc >>= 1
            crc_lo = crc & 0xFF
            crc_hi = (crc >> 8) & 0xFF
            full_frame = list(data) + [crc_lo, crc_hi]
            hex_data = " ".join(f"{b:02X}" for b in data)
            hex_full = " ".join(f"{b:02X}" for b in full_frame)
            out_write(out_crc, f"""
{'─'*58}
  Modbus CRC-16 Hesabı
{'─'*58}
  Giriş data : {hex_data}
  Byte sayısı: {len(data)}

  CRC-16      : 0x{crc:04X}  ({crc})
    Lo byte   : 0x{crc_lo:02X}  ({crc_lo})  → frame'e önce eklenir
    Hi byte   : 0x{crc_hi:02X}  ({crc_hi})  → sonra eklenir

  Tam frame (data + CRC Lo + CRC Hi):
    {hex_full}

  Doğrulama: Tam frame CRC hesaplanırsa → 0x0000 çıkmalı
{'─'*58}
""")
        except Exception as ex:
            out_write(out_crc, f"Hata: {ex}")

    calc_btn(fg_crc, "CRC-16 Hesapla", calc_crc16, row=1, col=0)

    # ── Modbus Frame Oluşturucu ──
    sub_lbl(inner, "▶ Modbus RTU Frame Oluşturucu")
    fg_mbf = tk.Frame(inner, bg=PANEL); fg_mbf.pack(fill="x", padx=12)
    e_mb_slave = lbl_entry(fg_mbf, "Slave ID (1-247):", "1",    row=0, col=0)
    e_mb_fc    = lbl_entry(fg_mbf, "FC (3/4/6/16...):", "3",    row=0, col=2)
    e_mb_addr  = lbl_entry(fg_mbf, "Başlangıç adres:", "0",    row=1, col=0)
    e_mb_count = lbl_entry(fg_mbf, "Kayıt sayısı/Değer:", "10", row=1, col=2)
    out_mbf = make_output(inner, 14)
    out_mbf.pack(fill="x", padx=12, pady=4)

    def build_modbus_frame():
        try:
            slave = int(e_mb_slave.get())
            fc    = int(e_mb_fc.get())
            addr  = int(e_mb_addr.get())
            count = int(e_mb_count.get())
            lines = []
            lines.append(f"{'─'*58}")
            lines.append(f"  Modbus RTU Frame — FC{fc:02d}")
            lines.append(f"{'─'*58}")

            if fc in (1, 2, 3, 4):  # Read
                data = [slave, fc,
                        (addr >> 8) & 0xFF, addr & 0xFF,
                        (count >> 8) & 0xFF, count & 0xFF]
                fc_names = {1:"Read Coils",2:"Read Discrete Inputs",
                            3:"Read Holding Registers",4:"Read Input Registers"}
                lines.append(f"  İşlem: {fc_names.get(fc, 'READ')}")
                lines.append(f"  Slave: {slave}, Adres: {addr} (0x{addr:04X}), Sayı: {count}")
                lines.append("")
                lines.append(f"  {'Alan':<22} {'Hex':>6}  {'Dec':>6}  Açıklama")
                labels = ["Slave Adres", "Fonksiyon Kodu",
                          "Adres Hi", "Adres Lo",
                          "Sayı Hi", "Sayı Lo"]
                for i, (b, lbl) in enumerate(zip(data, labels)):
                    lines.append(f"  [{i}] {lbl:<20} 0x{b:02X}  {b:6d}")
            elif fc == 6:  # Write Single Register
                val = count
                data = [slave, fc,
                        (addr >> 8) & 0xFF, addr & 0xFF,
                        (val >> 8) & 0xFF, val & 0xFF]
                lines.append(f"  İşlem: Write Single Register")
                lines.append(f"  Slave: {slave}, Adres: {addr}, Değer: {val}")
                lines.append("")
                labels = ["Slave Adres", "FC (0x06)",
                          "Adres Hi", "Adres Lo",
                          "Değer Hi", "Değer Lo"]
                for i, (b, lbl) in enumerate(zip(data, labels)):
                    lines.append(f"  [{i}] {lbl:<20} 0x{b:02X}  {b:6d}")
            else:
                data = [slave, fc,
                        (addr >> 8) & 0xFF, addr & 0xFF,
                        (count >> 8) & 0xFF, count & 0xFF]
                lines.append(f"  FC{fc} — Genel çerçeve gösterimi")
                for i, b in enumerate(data):
                    lines.append(f"  [{i}] 0x{b:02X}  ({b})")

            # CRC
            crc = 0xFFFF
            for byte in data:
                crc ^= byte
                for _ in range(8):
                    crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
            crc_lo, crc_hi = crc & 0xFF, (crc >> 8) & 0xFF
            data_crc = data + [crc_lo, crc_hi]
            lines.append(f"  [{len(data)}] CRC Lo             0x{crc_lo:02X}  {crc_lo:6d}")
            lines.append(f"  [{len(data)+1}] CRC Hi             0x{crc_hi:02X}  {crc_hi:6d}")
            lines.append("")
            lines.append("  Tam Frame (hex):")
            lines.append("  " + " ".join(f"{b:02X}" for b in data_crc))
            lines.append("")
            lines.append("  Python bytes:")
            lines.append(f"  b'\\x" + "\\x".join(f"{b:02x}" for b in data_crc) + "'")
            lines.append(f"{'─'*58}")
            out_write(out_mbf, "\n".join(lines))
        except Exception as ex:
            out_write(out_mbf, f"Hata: {ex}")

    calc_btn(fg_mbf, "Frame Oluştur", build_modbus_frame, row=2, col=0)
    return frame


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 8 — PROTOKOL KARŞILAŞTIRMA
# ═══════════════════════════════════════════════════════════════════════════════
def build_compare_tab(nb):
    frame = tk.Frame(nb, bg=PANEL)
    nb.add(frame, text="  Karşılaştırma  ")

    canvas = tk.Canvas(frame, bg=PANEL, highlightthickness=0)
    vsb = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(fill="both", expand=True)
    inner = tk.Frame(canvas, bg=PANEL)
    win_id = canvas.create_window((0,0), window=inner, anchor="nw")
    def on_conf(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(win_id, width=canvas.winfo_width())
    inner.bind("<Configure>", on_conf)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)),"units"))

    title_lbl(inner, "Haberleşme Protokolleri — Karşılaştırma Tablosu")

    headers = ["Protokol", "Kablo", "Hız", "Mesafe", "Cihaz sayısı", "Kullanım Alanı"]
    rows = [
        ["UART (TTL)",  "2 (TX,RX)",    "~1 Mbps",    "~1m",      "1-1",    "Debug, GPS, BT modül"],
        ["RS-232",      "2-9 arası",    "115.2 kbps", "~15m",     "1-1",    "PC, seri terminal"],
        ["RS-485",      "2 (A,B)",      "10 Mbps",    "1200m",    "32+",    "Modbus, Endüstri"],
        ["I2C",         "2 (SCL,SDA)",  "3.4 MHz",    "~3m",      "112",    "Sensör, EEPROM, OLED"],
        ["SPI",         "4 (4+CS)",     "100+ MHz",   "~1m",      "Sınırsız","SD kart, TFT, ADC"],
        ["CAN 2.0",     "2 (H,L)",      "1 Mbps",     "40-1000m", "110+",   "Otomotiv, robot"],
        ["CAN FD",      "2 (H,L)",      "8 Mbps",     "~40m",     "110+",   "Otomotiv (yeni)"],
        ["1-Wire",      "1 (data)",     "16.3 kbps",  "~300m",    "100+",   "DS18B20 sıcaklık"],
        ["LIN Bus",     "1 (data)",     "20 kbps",    "~40m",     "16",     "Araç içi düğmeler"],
        ["Ethernet",    "4-8 (RJ45)",   "10G+",       "100m",     "∞",      "Endüstriyel, IoT"],
        ["Modbus RTU",  "2 (RS-485)",   "115.2 kbps", "1200m",    "247",    "PLC, invertör, güç"],
        ["Modbus TCP",  "Ethernet",     "100 Mbps+",  "∞ (LAN)",  "∞",      "SCADA, uzak PLC"],
    ]
    col_colors = [ACCENT, GREEN, YELLOW, TEAL, MAUVE, PEACH]

    f_table = tk.Frame(inner, bg=PANEL2)
    f_table.pack(fill="x", padx=12, pady=8)
    for ci, h in enumerate(headers):
        tk.Label(f_table, text=h, bg=PANEL2, fg=col_colors[ci],
                 font=("Segoe UI", 9, "bold"), padx=6, pady=5,
                 relief="flat").grid(row=0, column=ci, sticky="ew", padx=1)
    for ri, row in enumerate(rows):
        bg = PANEL if ri % 2 == 0 else PANEL2
        for ci, val in enumerate(row):
            tk.Label(f_table, text=val, bg=bg, fg=FG,
                     font=("Consolas", 9), padx=6, pady=3,
                     anchor="w").grid(row=ri+1, column=ci, sticky="ew", padx=1)

    # Seçim rehberi
    sub_lbl(inner, "▶ Protokol Seçim Rehberi")
    choices = [
        ("Kart içi sensörler (≤5cm, az cihaz)", "→ I2C", GREEN),
        ("Kart içi yüksek hız (ADC, TFT, Flash)", "→ SPI", TEAL),
        ("Debug çıktısı, GPS, Bluetooth modülü",  "→ UART", YELLOW),
        ("Endüstriyel uzak cihaz (PLC, motor sürücü)", "→ RS-485 + Modbus RTU", PEACH),
        ("SCADA, fabrika ağı, IoT gateway", "→ Modbus TCP / EtherNet/IP", ACCENT),
        ("Otomotiv, çok-ECU sistemi, robot",  "→ CAN Bus", MAUVE),
        ("Çok cihaz, düşük maliyet, ortam verisi", "→ 1-Wire / LIN", FG2),
        ("PCB içi yüksek hız dijital (DDR, PCIe)", "→ Özel paralel/diferansiyel", RED),
    ]
    for situation, choice, color in choices:
        f = tk.Frame(inner, bg=PANEL2)
        f.pack(fill="x", padx=12, pady=2)
        tk.Label(f, text=f"  {situation:<48}", bg=PANEL2, fg=FG,
                 font=("Segoe UI", 9), padx=6, pady=4).pack(side="left")
        tk.Label(f, text=choice, bg=PANEL2, fg=color,
                 font=("Segoe UI", 9, "bold"), padx=6).pack(side="left")

    # EMI/Gürültü tavsiyeleri
    sub_lbl(inner, "▶ PCB EMC/EMI Tavsiyeleri")
    emc = [
        ("Decoupling kondansatör", "Her IC'nin VCC pinine 100nF seramik koyun (≤2mm iz)", GREEN),
        ("GND plane",             "Tüm referans düzlemini sürekli bakır plane yapın", TEAL),
        ("Diferansiyel hatlar",   "RS-485/CAN: Paralel, eşit uzunlukta, 100Ω diferansiyel", YELLOW),
        ("Via kullanımı",         "GND via grid'i gürültüyü bastırır. 1.6mm kartda 0.3mm via", ACCENT),
        ("Kristal/osilatör",      "GND ile çevrelenmiş, kısa iz, altında via ile GND'ye bağlı", MAUVE),
        ("Yüksek akım izleri",    "Güç izlerini en kısa tut, geniş yap. GND döngüsünü küçük tut", PEACH),
        ("ESD koruması",          "Harici bağlantılara TVS diyot/ESD süpresör ekleyin", RED),
        ("Filtreleme",            "Güç girişine ferrit boncuk (bead) + 100µF bulk kondansatör", FG2),
    ]
    for title, desc, color in emc:
        f = tk.Frame(inner, bg=PANEL2)
        f.pack(fill="x", padx=12, pady=2)
        tk.Label(f, text=f"  {title:<26}", bg=PANEL2, fg=color,
                 font=("Segoe UI", 9, "bold"), padx=6, pady=4).pack(side="left")
        tk.Label(f, text=desc, bg=PANEL2, fg=FG,
                 font=("Segoe UI", 9), padx=4).pack(side="left")

    return frame


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 9 — MİNİ UYGULAMALAR
# ═══════════════════════════════════════════════════════════════════════════════
def build_apps_tab(nb):
    frame = tk.Frame(nb, bg=PANEL)
    nb.add(frame, text="  Mini Uygulamalar  ")

    canvas = tk.Canvas(frame, bg=PANEL, highlightthickness=0)
    vsb = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(fill="both", expand=True)
    inner = tk.Frame(canvas, bg=PANEL)
    win_id = canvas.create_window((0,0), window=inner, anchor="nw")
    def on_conf(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(win_id, width=canvas.winfo_width())
    inner.bind("<Configure>", on_conf)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)),"units"))

    title_lbl(inner, "Mini Uygulamalar & Pratik Araçlar")

    # ── 1. LED Direnç Hesaplayıcı ──
    sub_lbl(inner, "▶ APP 1 — LED Direnç Hesaplayıcı")
    info_box(inner, "R = (Vsupply - Vf) / If\nVf: Kırmızı≈2.0V, Sarı≈2.1V, Yeşil≈2.2V, Mavi/Beyaz≈3.2V", YELLOW)
    fg_led = tk.Frame(inner, bg=PANEL); fg_led.pack(fill="x", padx=12)
    e_vs   = lbl_entry(fg_led, "Vcc (V):",       "5",   row=0, col=0)
    e_vf   = lbl_entry(fg_led, "Vf LED (V):",    "2.0", row=0, col=2)
    e_if   = lbl_entry(fg_led, "If hedef (mA):", "10",  row=1, col=0)
    e_leds = lbl_entry(fg_led, "LED sayısı (seri):", "1", row=1, col=2)
    out_led = make_output(inner, 8)
    out_led.pack(fill="x", padx=12, pady=4)

    def calc_led():
        try:
            Vs   = float(e_vs.get())
            Vf   = float(e_vf.get())
            If_  = float(e_if.get()) / 1000
            nleds= int(e_leds.get())
            Vtot = Vf * nleds
            if Vs <= Vtot:
                out_write(out_led, f"⚠ Vcc ({Vs}V) ≤ Toplam Vf ({Vtot}V)! Voltaj yetersiz."); return
            R = (Vs - Vtot) / If_
            P = If_**2 * R
            Pd_led = Vf * If_
            out_write(out_led, f"""
{'─'*50}
  LED Direnç Hesabı
{'─'*50}
  Vcc       = {Vs} V
  Vf / LED  = {Vf} V × {nleds} adet = {Vtot} V toplam
  If hedef  = {If_*1000:.1f} mA

  Hesaplanan R = (Vcc - Vf_toplam) / If
               = ({Vs} - {Vtot}) / {If_*1000:.1f}mA
               = {R:.1f} Ω

  E24 standart: {e24_nearest(R)}
  Güç (R)   = {P*1000:.2f} mW  (en az {math.ceil(P*4/0.25)*250}mW direnç seç)
  Güç / LED = {Pd_led*1000:.2f} mW

  Brightness: {'Parlak' if If_*1000 >= 15 else 'Orta' if If_*1000 >= 5 else 'Zayıf'} ({If_*1000:.1f}mA)
{'─'*50}
""")
        except Exception as ex:
            out_write(out_led, f"Hata: {ex}")

    calc_btn(fg_led, "LED Direnci Hesapla", calc_led, row=2, col=0)

    # ── 2. Frekans → Period Dönüştürücü ──
    sub_lbl(inner, "▶ APP 2 — Frekans ↔ Periyot ↔ Dalga Boyu Dönüştürücü")
    fg_freq = tk.Frame(inner, bg=PANEL); fg_freq.pack(fill="x", padx=12)
    e_freq_in = lbl_entry(fg_freq, "Frekans (Hz):", "1000000", row=0, col=0, width=16)
    out_freq = make_output(inner, 10)
    out_freq.pack(fill="x", padx=12, pady=4)

    def conv_freq():
        try:
            f = float(e_freq_in.get())
            T = 1 / f
            lam = 3e8 / f  # dalga boyu (havada)
            lam_pcb = 3e8 / (f * math.sqrt(4.4))  # FR4'te
            quarter = lam_pcb / 4
            refs = {50:"AM Radyo", 88e6:"FM Alt", 108e6:"FM Üst",
                    2.4e9:"WiFi/BT", 5e9:"WiFi 5GHz", 1e3:"1kHz ses",
                    20e3:"Ultrason", 1e6:"1MHz kristal"}
            closest_ref = min(refs.items(), key=lambda x: abs(x[0]-f))
            out_write(out_freq, f"""
{'─'*55}
  Frekans / Periyot / Dalga Boyu
{'─'*55}
  Frekans : {f:.6g} Hz
           = {f/1000:.6g} kHz
           = {f/1e6:.6g} MHz
           = {f/1e9:.6g} GHz

  Periyot : {T:.6g} s
           = {T*1000:.6g} ms
           = {T*1e6:.6g} µs
           = {T*1e9:.6g} ns

  Dalga Boyu (havada, c=3×10⁸ m/s):
    λ       = {lam:.4g} m  ({lam*100:.4g} cm)
    λ/4     = {lam/4*100:.4g} cm  (çeyrek dalga anteni)

  Dalga Boyu (FR4 PCB, εr=4.4):
    λ_pcb   = {lam_pcb:.4g} m  ({lam_pcb*100:.4g} cm)
    λ/4 PCB = {quarter*100:.4g} cm  (izole iz boyutu)

  Referans: {closest_ref[1]} ≈ {closest_ref[0]:.3g} Hz
{'─'*55}
""")
        except Exception as ex:
            out_write(out_freq, f"Hata: {ex}")

    calc_btn(fg_freq, "Dönüştür", conv_freq, row=1, col=0)

    # ── 3. Hex / Binary / Decimal Dönüştürücü ──
    sub_lbl(inner, "▶ APP 3 — Sayı Sistemi Dönüştürücü (HEX / BIN / DEC / OCT)")
    fg_num = tk.Frame(inner, bg=PANEL); fg_num.pack(fill="x", padx=12)
    e_num_in   = lbl_entry(fg_num, "Değer:", "255", row=0, col=0, width=20)
    e_num_base = lbl_entry(fg_num, "Taban (10/16/2/8):", "10", row=0, col=2, width=5)
    out_num = make_output(inner, 10)
    out_num.pack(fill="x", padx=12, pady=4)

    def conv_num():
        try:
            base = int(e_num_base.get())
            val  = int(e_num_in.get().strip(), base)
            signed16 = val if val < 32768 else val - 65536
            signed32 = val if val < 2**31 else val - 2**32
            out_write(out_num, f"""
{'─'*55}
  Sayı Sistemi Dönüşümü
{'─'*55}
  Giriş (taban {base}): {e_num_in.get().strip()}

  Decimal (10) : {val}
  Hexadecimal  : 0x{val:X}
    (8-bit)    : 0x{val & 0xFF:02X}
    (16-bit)   : 0x{val & 0xFFFF:04X}
    (32-bit)   : 0x{val & 0xFFFFFFFF:08X}
  Binary       : 0b{val:b}
    (8-bit)    :   {val & 0xFF:08b}b = {' '.join(f'{(val>>i)&1}' for i in range(7,-1,-1))}
    (16-bit)   :   {val & 0xFFFF:016b}b
  Octal        : 0o{val:o}

  İşaretli yorumlar:
    INT8  (signed 8-bit) : {(val&0xFF) if (val&0xFF)<128 else (val&0xFF)-256}
    INT16 (signed 16-bit): {signed16 if val <= 0xFFFF else '?'}
    INT32 (signed 32-bit): {signed32 if val <= 0xFFFFFFFF else '?'}

  ASCII: {''.join(chr(val & 0xFF) if 32 <= (val & 0xFF) < 127 else '.' )}
{'─'*55}
""")
        except Exception as ex:
            out_write(out_num, f"Hata: {ex}")

    calc_btn(fg_num, "Dönüştür", conv_num, row=1, col=0)

    # ── 4. Kondansatör Enerji & Şarj ──
    sub_lbl(inner, "▶ APP 4 — Kondansatör Hesaplayıcı")
    info_box(inner,
             "E = ½·C·V²  |  τ = R·C  |  V(t) = Vs·(1 - e^(-t/τ))\n"
             "Şarj: 63.2% → 1τ, 86.5% → 2τ, 95% → 3τ, 98.2% → 4τ, 99.3% → 5τ", TEAL)
    fg_cap = tk.Frame(inner, bg=PANEL); fg_cap.pack(fill="x", padx=12)
    e_cap_C  = lbl_entry(fg_cap, "C (µF):",    "100", row=0, col=0)
    e_cap_V  = lbl_entry(fg_cap, "V (Volt):",  "12",  row=0, col=2)
    e_cap_R  = lbl_entry(fg_cap, "R (Ohm, şarj):", "1000", row=1, col=0)
    out_cap = make_output(inner, 12)
    out_cap.pack(fill="x", padx=12, pady=4)

    def calc_cap():
        try:
            C  = float(e_cap_C.get()) * 1e-6
            V  = float(e_cap_V.get())
            R  = float(e_cap_R.get())
            E  = 0.5 * C * V**2
            tau= R * C
            lines = [f"{'─'*55}", "  Kondansatör Analizi", f"{'─'*55}",
                     f"  C = {C*1e6:.4g} µF  ({C*1e9:.4g} nF)",
                     f"  V = {V} V",
                     f"  R = {R:.4g} Ω (şarj direnci)",
                     "",
                     f"  Enerji   : E = ½CV² = {E*1e3:.4g} mJ  ({E*1e6:.4g} µJ)",
                     f"  Zaman sab: τ = RC  = {tau*1000:.4g} ms  ({tau*1e6:.4g} µs)",
                     "",
                     "  Şarj Zaman Tablosu:",
                     f"  {'τ':>4}  {'Süre':>10}  {'Gerilim':>10}  {'%':>6}",
                     f"  {'─'*40}"]
            for n in [0.5, 1, 2, 3, 4, 5]:
                t = n * tau
                Vt = V * (1 - math.exp(-n))
                pct = Vt / V * 100
                t_str = f"{t*1000:.3f}ms" if t >= 1e-3 else f"{t*1e6:.1f}µs"
                lines.append(f"  {n:>4.1f}τ  {t_str:>10}  {Vt:>9.4f}V  {pct:>5.1f}%")
            lines.append("")
            lines.append(f"  Tam şarj (5τ): {5*tau*1000:.3f} ms")
            lines.append(f"{'─'*55}")
            out_write(out_cap, "\n".join(lines))
        except Exception as ex:
            out_write(out_cap, f"Hata: {ex}")

    calc_btn(fg_cap, "Kondansatör Hesapla", calc_cap, row=2, col=0)

    return frame


# ═══════════════════════════════════════════════════════════════════════════════
# ANA UYGULAMA
# ═══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PCB & Haberleşme Rehberi — Başlangıç & Orta Düzey")
        self.configure(bg=PANEL)
        self.geometry("960x720")
        self.minsize(800, 600)

        # Başlık
        header = tk.Frame(self, bg=ACCENT, height=44)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="  ⚡ PCB & Haberleşme Rehberi",
                 font=("Segoe UI", 13, "bold"),
                 bg=ACCENT, fg=BG).pack(side="left", padx=8)
        tk.Label(header, text="Hesaplama · Protokol Simülatörü · Mini Uygulamalar",
                 font=("Segoe UI", 9),
                 bg=ACCENT, fg="#1a1a2e").pack(side="left")

        # Notebook
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab",
                        background=PANEL2, foreground=FG2,
                        font=("Segoe UI", 9, "bold"),
                        padding=[10, 5])
        style.map("TNotebook.Tab",
                  background=[("selected", PANEL), ("active", ENTRY)],
                  foreground=[("selected", ACCENT), ("active", FG)])

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=0, pady=0)

        build_pcb_tab(nb)
        build_guc_tab(nb)
        build_uart_tab(nb)
        build_i2c_tab(nb)
        build_spi_tab(nb)
        build_can_tab(nb)
        build_modbus_tab(nb)
        build_compare_tab(nb)
        build_apps_tab(nb)

        # Durum çubuğu
        status = tk.Frame(self, bg=PANEL2, height=22)
        status.pack(fill="x", side="bottom")
        status.pack_propagate(False)
        tk.Label(status,
                 text="  Sekmeleri keşfet → PCB | Güç | UART | I2C | SPI | CAN | Modbus | Karşılaştırma | Mini Uygulamalar",
                 bg=PANEL2, fg=FG3, font=("Segoe UI", 8)).pack(side="left")


if __name__ == "__main__":
    App().mainloop()

