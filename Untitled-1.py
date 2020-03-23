dataPolya = pd.read_csv('MADAGASCAR/polya_pre_weighted_heur_deg_ck.csv', header=None).values.tolist()
In = []
for j in range(len(dataPolya)):
    In.append(dataPolya[j][0])
plt.plot(range(max_n), In, label=legend[i])
#plt.plot(range(max_n), dataSIS, label='SIS'+legend[i])
plt.xlabel('Time (n)')
plt.ylabel('Infection Rate $\\tilde{I}_n$')

plt.title(title)
plt.legend()
plt.show()