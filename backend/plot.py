import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.pyplot as plt
plt.ion()  # Включить интерактивный режим
# Параметры первого распределения (ручной сбор)
mu_manual = 54
sigma_manual = 10  # предположим стандартное отклонение (можно заменить на реальное)

# Параметры второго распределения (автоматический сбор)
data_auto = [3.14, 2.87, 2.35, 2.69, 2.01, 2.78, 2.42, 2.95, 2.22, 2.58, 2.10]
mu_auto = np.mean(data_auto)  # ~2.46
sigma_auto = np.std(data_auto, ddof=1)  # выборочное стандартное отклонение

# Создаём сетку значений для графика, охватывающую оба распределения
x = np.linspace(0, 80, 1000)

# Плотности вероятности
pdf_manual = norm.pdf(x, mu_manual, sigma_manual)
pdf_auto = norm.pdf(x, mu_auto, sigma_auto)

plt.figure(figsize=(10,6))

# Графики плотностей
plt.plot(x, pdf_manual, label=f'Ручной сбор (μ={mu_manual}, σ={sigma_manual:.2f})', color='blue')
plt.plot(x, pdf_auto, label=f'Автоматический сбор (μ={mu_auto:.2f}, σ={sigma_auto:.2f})', color='orange')

# Отметки ±3σ для ручного сбора
plt.axvline(mu_manual - 3*sigma_manual, color='blue', linestyle='--', alpha=0.5)
plt.axvline(mu_manual + 3*sigma_manual, color='blue', linestyle='--', alpha=0.5)

# Отметки ±3σ для автоматического сбора
plt.axvline(mu_auto - 3*sigma_auto, color='orange', linestyle='--', alpha=0.5)
plt.axvline(mu_auto + 3*sigma_auto, color='orange', linestyle='--', alpha=0.5)

# Подписи и легенда
plt.title('Сравнение нормальных распределений времени сбора НПА')
plt.xlabel('Время (секунды)')
plt.ylabel('Плотность вероятности')
plt.legend()
plt.grid(True)
plt.show()
plt.savefig('plot.png')
