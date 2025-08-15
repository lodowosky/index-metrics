import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#input
summary = pd.read_csv('summary.csv', index_col=0) 
cumulative_returns_outer = pd.read_csv('cumulative_returns_outer.txt', index_col=0)
aligned_returns = cumulative_returns_outer.dropna() 

x_annual_aligned = pd.Series(aligned_returns.iloc[:, 0], name=aligned_returns.columns[0])
y_annual_aligned = pd.Series(aligned_returns.iloc[:, 1], name=aligned_returns.columns[1])
z_annual_aligned = pd.Series(aligned_returns.iloc[:, 2], name=aligned_returns.columns[2])
w_annual_aligned = pd.Series(aligned_returns.iloc[:, 3], name=aligned_returns.columns[3])

x_label = aligned_returns.columns[0]
y_label = aligned_returns.columns[1]
z_label = aligned_returns.columns[2]
w_label = aligned_returns.columns[3]


x_dev_std = summary.iloc[0, 4]
y_dev_std = summary.iloc[1, 4]
z_dev_std = summary.iloc[2, 4]
w_dev_std = summary.iloc[3, 4]

rendimenti = []
dev_std = []
sharpe_ratios = []

quote_x = []
quote_y = []
quote_z = []
quote_w = []

# Iterazione per trovare varie combinazioni di quote per x, y, z e w
for i in np.arange(0.1, 0.9, 0.05):
    for j in np.arange(0.1, 0.9, 0.05):
        for k in np.arange(0.1, 0.9, 0.05):
            if i + j + k < 1:
                quota_x = i
                quota_y = j
                quota_z = k
                quota_w = 1 - quota_x - quota_y - quota_z

                # Analisi bilanciamento portfolio
                portfolio_annual = (x_annual_aligned * quota_x +
                                    y_annual_aligned * quota_y +
                                    z_annual_aligned * quota_z +
                                    w_annual_aligned * quota_w)
                p_rendimento_atteso = np.mean(portfolio_annual)

                # Calcolo della varianza del portafoglio
                portfolio_variance = (quota_x ** 2 * x_dev_std ** 2 +
                                      quota_y ** 2 * y_dev_std ** 2 +
                                      quota_z ** 2 * z_dev_std ** 2 +
                                      quota_w ** 2 * w_dev_std ** 2 +
                                      2 * quota_x * quota_y * x_dev_std * y_dev_std * np.corrcoef(x_annual_aligned, y_annual_aligned)[0, 1] +
                                      2 * quota_x * quota_z * x_dev_std * z_dev_std * np.corrcoef(x_annual_aligned, z_annual_aligned)[0, 1] +
                                      2 * quota_x * quota_w * x_dev_std * w_dev_std * np.corrcoef(x_annual_aligned, w_annual_aligned)[0, 1] +
                                      2 * quota_y * quota_z * y_dev_std * z_dev_std * np.corrcoef(y_annual_aligned, z_annual_aligned)[0, 1] +
                                      2 * quota_y * quota_w * y_dev_std * w_dev_std * np.corrcoef(w_annual_aligned, y_annual_aligned)[0, 1] +
                                      2 * quota_z * quota_w * z_dev_std * w_dev_std * np.corrcoef(w_annual_aligned, z_annual_aligned)[0, 1])

                # Calcolo della deviazione standard del portafoglio (rischio)
                p_std_dev = np.sqrt(portfolio_variance)
                p_sharpe_ratio = p_rendimento_atteso / p_std_dev

                print(f"Portfolio ({x_label}={quota_x*100:.0f}%, {y_label}={quota_y*100:.0f}%, {z_label}={quota_z*100:.0f}%, {w_label}={quota_w*100:.0f}%) = {p_rendimento_atteso:.5f} +- {p_std_dev:.5f}; Sharpe ratio =  {p_sharpe_ratio:.5f}")

                plt.scatter(p_std_dev, p_rendimento_atteso, color="#BBE6E4", alpha=0.75)
                rendimenti.append(p_rendimento_atteso)
                dev_std.append(p_std_dev)
                sharpe_ratios.append(p_sharpe_ratio)


                quote_x.append(quota_x)
                quote_y.append(quota_y)
                quote_z.append(quota_z)
                quote_w.append(quota_w)

# Calcolo del rischio minimo e dei valori corrispondenti
dev_std_min = min(dev_std)
indice_min = dev_std.index(dev_std_min)
rend_corrispondente_ds = rendimenti[indice_min]
sharpe_ratio_corr_ds = sharpe_ratios[indice_min]

quota_x_corr_ds = quote_x[indice_min]
quota_y_corr_ds = quote_y[indice_min]
quota_z_corr_ds = quote_z[indice_min]
quota_w_corr_ds = quote_w[indice_min]

# Calcolo del l'indice di sharpe massimo e dei valori corrispondenti
sharpe_ratio_max = max(sharpe_ratios)
indice_max = sharpe_ratios.index(sharpe_ratio_max)
rend_corrispondente_sr = rendimenti[indice_max]
dev_std_corr_sr = dev_std[indice_max]

quota_x_corr_sr = quote_x[indice_max]
quota_y_corr_sr = quote_y[indice_max]
quota_z_corr_sr = quote_z[indice_max]
quota_w_corr_sr = quote_w[indice_max]

print()
print(f'Calcolo della composizione ottimale minimizzando il rischio')
print()
print(f'Portfolio meno rischioso ({x_label}={quota_x_corr_ds*100:.0f}%, {y_label}={quota_y_corr_ds*100:.0f}%, {z_label}={quota_z_corr_ds*100:.0f}%, {w_label}={quota_w_corr_ds*100:.0f}%) = {rend_corrispondente_ds:.5f} +- {dev_std_min:.5f}; Sharpe ratio = {sharpe_ratio_corr_ds:.2f}')
print(f'Portfolio efficiente ({x_label}={quota_x_corr_sr*100:.0f}%, {y_label}={quota_y_corr_sr*100:.0f}%, {z_label}={quota_z_corr_sr*100:.0f}%, {w_label}={quota_w_corr_sr*100:.0f}%) = {rend_corrispondente_sr:.5f} +- {dev_std_corr_sr:.5f}; Sharpe ratio = {sharpe_ratio_max:.2f}')

p_label_ds=f'Portfolio meno rischioso : {rend_corrispondente_ds:.2f}% +- {dev_std_min:.2f}%; Sharpe ratio = {sharpe_ratio_corr_ds:.2f}'
plt.scatter(dev_std_min, rend_corrispondente_ds, label=p_label_ds, color='c')

p_label_sr=f'Portfolio efficiente : {rend_corrispondente_sr:.2f}% +- {dev_std_corr_sr:.2f}%; Sharpe ratio = {sharpe_ratio_max:.2f}'
plt.scatter(dev_std_corr_sr, rend_corrispondente_sr, label=p_label_sr, color = 'red', alpha = 0.5)

plt.xlabel("Volatilità dei rendimenti")
plt.ylabel("Rendimento annuale atteso (%)")
plt.axis('equal')
plt.legend(loc='best')
plt.grid(True)

# Mostrare il grafico
plt.show()
