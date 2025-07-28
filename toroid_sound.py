import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine

# Constantes físicas
c = 299_792_458  # velocidade da luz (m/s)
r = 1e12         # raio do toroide (muito grande → simula infinito)
duration_ms = 60_000  # duração total em milissegundos
num_pulses = 100       # número de "wOOmmm"
max_wr_over_c = 0.99   # evitar ultrapassar c
max_w = (max_wr_over_c * c) / r

# Lista de segmentos de som
segments = []

# Gera pulsos com base na equação relativística
for i in range(num_pulses):
    w = 0.01 + (i / num_pulses) * max_w
    wr_over_c = (w * r) / c
    if wr_over_c >= 1:
        continue  # evita raiz de número negativo

    v = (4 * w * r) / (np.pi * np.sqrt(1 - wr_over_c ** 2))

    # Frequência audível entre 50 e 300 Hz
    freq = np.interp(v, [0, (4 * c) / np.pi], [50, 300])

    # Duração do pulso e pausa (acelera com o tempo)
    pulse_duration_ms = int(np.interp(i, [0, num_pulses], [300, 30]))
    pause_duration_ms = int(np.interp(i, [0, num_pulses], [200, 10]))

    # Gera o som da volta e uma pausa
    pulse = Sine(freq).to_audio_segment(duration=pulse_duration_ms).fade_out(30)
    pause = AudioSegment.silent(duration=pause_duration_ms)
    segments.append(pulse + pause)

# Combina os segmentos
toroid_audio = sum(segments)

# Gera vibração contínua final
v_final = (4 * max_w * r) / (np.pi * np.sqrt(1 - max_wr_over_c ** 2))
freq_final = np.interp(v_final, [0, (4 * c) / np.pi], [50, 300])
vibration = Sine(freq_final).to_audio_segment(duration=1000).fade_in(100).fade_out(100)

# Preenche até 60 segundos
while len(toroid_audio) + len(vibration) < duration_ms:
    toroid_audio += vibration

# Corta exatamente em 60 segundos
final_audio = toroid_audio[:duration_ms]

# Exporta para MP3
final_audio.export("toroide_tesoura_loop.mp3", format="mp3")
print("✅ Áudio gerado: toroide_tesoura_loop.mp3")
