import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter, find_peaks


# CONFIGURACIÓN
modo      = "archivo"   # "captura" o "archivo"
fs        = 500
duracion  = 240         # segundos
archivo   = "ECG1.txt"
archivo_f = "ECG1_filtrada.txt"


# OBTENER SEÑAL
if modo == "captura":
    import nidaqmx
    from nidaqmx.constants import AcquisitionType

    total_muestras = int(fs * duracion)

    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan('Dev4/ai0')
        task.timing.cfg_samp_clk_timing(fs, sample_mode=AcquisitionType.FINITE,
                                        samps_per_chan=total_muestras)
        senal_total = np.array(task.read(number_of_samples_per_channel=total_muestras))

    t_total = np.arange(len(senal_total)) / fs

   # FILTRO IIR PASA BANDA ECG
    fc_low  = 0.5
    fc_high = 40
    orden   = 4   # Orden del filtro

    b, a  = butter(orden, [fc_low/(fs/2), fc_high/(fs/2)], btype='bandpass')
    ecg_f = lfilter(b, a, senal_total)
    
    # guardar archivo
    np.savetxt(archivo,   np.column_stack((t_total, senal_total)), delimiter=",", header="Tiempo(s),ECG(V)", comments="")
    np.savetxt(archivo_f, np.column_stack((t_total, ecg_f)),       delimiter=",", header="Tiempo(s),ECG(V)", comments="")
    print("Captura finalizada y archivos guardados.")

else:
    raw   = np.loadtxt(archivo,   delimiter=",", skiprows=1)
    filt  = np.loadtxt(archivo_f, delimiter=",", skiprows=1)
    t_total, senal_total, ecg_f = raw[:,0], raw[:,1], filt[:,1]
    fs    = 1 / np.mean(np.diff(t_total))
    print(f"Archivos cargados: {len(t_total)} muestras ({len(t_total)/fs:.1f} s)")

# PARTE B – SEGMENTACIÓN Y DETECCIÓN DE PICOS R
n2m = int(2 * 60 * fs)
n15 = int(15 * fs)

seg1, t1 = ecg_f[:n2m],      t_total[:n2m]
seg2, t2 = ecg_f[n2m:2*n2m], t_total[n2m:2*n2m]

def picos_R(seg, fs):
    p, _ = find_peaks(seg, height=0.6*np.max(seg), distance=int(0.3*fs))
    return p

p1, p2 = picos_R(seg1, fs), picos_R(seg2, fs)
rr1     = np.diff(p1) / fs * 1000
rr2     = np.diff(p2) / fs * 1000

print("\n===== HRV – DOMINIO DEL TIEMPO =====")
print(f"  Reposo  → Media R-R: {np.mean(rr1):.2f} ms | SDNN: {np.std(rr1, ddof=1):.2f} ms")
print(f"  Lectura → Media R-R: {np.mean(rr2):.2f} ms | SDNN: {np.std(rr2, ddof=1):.2f} ms")


# PARTE C – POINCARÉ
def poincare(rr):
    sd1 = np.std((rr[1:]-rr[:-1])/np.sqrt(2), ddof=1)
    sd2 = np.std((rr[1:]+rr[:-1])/np.sqrt(2), ddof=1)
    return sd1, sd2, sd2/sd1, np.log10(sd1*sd2)

sd1_1, sd2_1, csi1, cvi1 = poincare(rr1)
sd1_2, sd2_2, csi2, cvi2 = poincare(rr2)

print("\n===== POINCARÉ =====")
print(f"  Reposo  → SD1: {sd1_1:.2f} | SD2: {sd2_1:.2f} | CSI: {csi1:.3f} | CVI: {cvi1:.3f}")
print(f"  Lectura → SD1: {sd1_2:.2f} | SD2: {sd2_2:.2f} | CSI: {csi2:.3f} | CVI: {cvi2:.3f}")


# GRÁFICAS
def plot_ecg(t, seg, picos, titulo, color, solo_15s=False):
    if solo_15s:
        t_plot, s_plot = t[:n15], seg[:n15]
        p_plot = picos[picos < n15]
    else:
        t_plot, s_plot = t, seg
        p_plot = picos

    plt.figure(figsize=(14, 4))
    plt.plot(t_plot, s_plot, color=color, linewidth=0.8)
    plt.plot(t_plot[p_plot], s_plot[p_plot], 'k^', markersize=5, label='Picos R')
    plt.title(titulo, fontweight='bold')
    plt.xlabel("Tiempo [s]"); plt.ylabel("Voltaje [V]")
    plt.legend(); plt.grid(True, alpha=0.3); plt.tight_layout(); plt.show()

def plot_poincare(rr, sd1, sd2, csi, cvi, titulo, color):
    ang  = np.linspace(0, 2*np.pi, 200)
    e1   = np.array([ np.cos(np.pi/4), np.sin(np.pi/4)])
    e2   = np.array([-np.sin(np.pi/4), np.cos(np.pi/4)])
    elip = sd1 * np.outer(np.sin(ang), e2) + sd2 * np.outer(np.cos(ang), e1)
    cx, cy = np.mean(rr[:-1]), np.mean(rr[1:])

    plt.figure(figsize=(6, 6))
    plt.scatter(rr[:-1], rr[1:], s=12, alpha=0.6, color=color)
    plt.plot(cx + elip[:,0], cy + elip[:,1], 'k--', linewidth=1.2)
    plt.title(titulo, fontweight='bold')
    plt.xlabel("RR$_n$ [ms]"); plt.ylabel("RR$_{n+1}$ [ms]")
    plt.gca().text(0.03, 0.97, f"SD1={sd1:.1f}\nSD2={sd2:.1f}\nCSI={csi:.3f}\nCVI={cvi:.3f}",
                   transform=plt.gca().transAxes, va='top',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    plt.gca().set_aspect('equal', adjustable='datalim')
    plt.grid(True, alpha=0.3); plt.tight_layout(); plt.show()

# ECG completo 2 minutos
plot_ecg(t1, seg1, p1, "ECG – Reposo (2 min)",              'steelblue', solo_15s=False)
plot_ecg(t2, seg2, p2, "ECG – Lectura en voz alta (2 min)", 'tomato',    solo_15s=False)

# ECG muestra 15 s
plot_ecg(t1, seg1, p1, "ECG – Reposo (15 s)",              'steelblue', solo_15s=True)
plot_ecg(t2, seg2, p2, "ECG – Lectura en voz alta (15 s)",  'tomato',   solo_15s=True)

# Serie R-R
plt.figure(figsize=(12, 4))
plt.plot(rr1, color='steelblue', linewidth=0.9, label='Reposo')
plt.plot(rr2, color='tomato',    linewidth=0.9, label='Lectura')
plt.title("Serie R-R comparada", fontweight='bold')
plt.xlabel("Latido #"); plt.ylabel("Intervalo R-R [ms]")
plt.legend(); plt.grid(True, alpha=0.3); plt.tight_layout(); plt.show()

# Poincaré
plot_poincare(rr1, sd1_1, sd2_1, csi1, cvi1, "Poincaré – Reposo",             'steelblue')
plot_poincare(rr2, sd1_2, sd2_2, csi2, cvi2, "Poincaré – Lectura en voz alta", 'tomato')

print("\nAnálisis HRV completado.")