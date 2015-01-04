cc_t1t1 = np.loadtxt("jaccard_boxplot_syncc_t1t1.txt")
cc_t2t2 = np.loadtxt("jaccard_boxplot_syncc_t2t2.txt")
cc_pdpd = np.loadtxt("jaccard_boxplot_syncc_pdpd.txt")
cc_t1t2 = np.loadtxt("jaccard_boxplot_syncc_t1t2.txt")
cc_t1pd = np.loadtxt("jaccard_boxplot_syncc_t1pd.txt")
cc_t2pd = np.loadtxt("jaccard_boxplot_syncc_t2pd.txt")
ecc_t1t1 = np.loadtxt("jaccard_boxplot_synecc_t1t1.txt")
ecc_t2t2 = np.loadtxt("jaccard_boxplot_synecc_t2t2.txt")
ecc_pdpd = np.loadtxt("jaccard_boxplot_synecc_pdpd.txt")
ecc_t1t2 = np.loadtxt("jaccard_boxplot_synecc_t1t2.txt")
ecc_t1pd = np.loadtxt("jaccard_boxplot_synecc_t1pd.txt")
ecc_t2pd = np.loadtxt("jaccard_boxplot_synecc_t2pd.txt")
em_t1t1 = np.loadtxt("jaccard_boxplot_synem_t1t1.txt")
em_t2t2 = np.loadtxt("jaccard_boxplot_synem_t2t2.txt")
em_pdpd = np.loadtxt("jaccard_boxplot_synem_pdpd.txt")
em_t1t2 = np.loadtxt("jaccard_boxplot_synem_t1t2.txt")
em_t1pd = np.loadtxt("jaccard_boxplot_synem_t1pd.txt")
em_t2pd = np.loadtxt("jaccard_boxplot_synem_t2pd.txt")
mi_t1t1 = np.loadtxt("jaccard_boxplot_synmi_t1t1.txt")
mi_t2t2 = np.loadtxt("jaccard_boxplot_synmi_t2t2.txt")
mi_pdpd = np.loadtxt("jaccard_boxplot_synmi_pdpd.txt")
mi_t1t2 = np.loadtxt("jaccard_boxplot_synmi_t1t2.txt")
mi_t1pd = np.loadtxt("jaccard_boxplot_synmi_t1pd.txt")
mi_t2pd = np.loadtxt("jaccard_boxplot_synmi_t2pd.txt")

######T1-T1####
t1t1_scores = [cc_t1t1, ecc_t1t1, em_t1t1, mi_t1t1]
t1t1_names = ["CC", "ECC", "EM", "MI"]
fig, ax1 = plt.subplots()
boxplot(t1t1_scores)
ax1.set_axisbelow(True)
ax1.set_title('Distribution of mean Jaccard scores (averaged over 31 regions per pair). Registration of 301 T1-T1 pairs.')
ax1.set_ylabel('Mean Jaccard index')
ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
ax1.set_ylim(0.3, 0.8)
xtick_names = setp(ax1, xticklabels=t1t1_names)
setp(xtick_names, rotation=45, fontsize=16)

######T2-T2####
t2t2_scores = [cc_t2t2, ecc_t2t2, em_t2t2, mi_t2t2]
t2t2_names = ["CC", "ECC", "EM", "MI"]
fig, ax1 = plt.subplots()
boxplot(t2t2_scores)
ax1.set_axisbelow(True)
ax1.set_title('Distribution of mean Jaccard scores (averaged over 31 regions per pair). Registration of 301 T2-T2 pairs.')
ax1.set_ylabel('Mean Jaccard index')
ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
ax1.set_ylim(0.3, 0.8)
xtick_names = setp(ax1, xticklabels=t2t2_names)
setp(xtick_names, rotation=45, fontsize=16)

######PD-PD####
pdpd_scores = [cc_pdpd, ecc_pdpd, em_pdpd, mi_pdpd]
pdpd_names = ["CC", "ECC", "EM", "MI"]
fig, ax1 = plt.subplots()
boxplot(pdpd_scores)
ax1.set_axisbelow(True)
ax1.set_title('Distribution of mean Jaccard scores (averaged over 31 regions per pair). Registration of 301 PD-PD pairs.')
ax1.set_ylabel('Mean Jaccard index')
ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
ax1.set_ylim(0.3, 0.8)
xtick_names = setp(ax1, xticklabels=pdpd_names)
setp(xtick_names, rotation=45, fontsize=16)

######T1-T2####
t1t2_scores = [cc_t1t1, cc_t1t2, ecc_t1t2, em_t1t2, mi_t1t2]
t1t2_names = ["Baseline", "CC", "ECC", "EM", "MI"]
fig, ax1 = plt.subplots()
boxplot(t1t2_scores)
ax1.set_axisbelow(True)
ax1.set_title('Distribution of mean Jaccard scores (averaged over 31 regions per pair). Registration of 612 T1-T2 pairs.')
ax1.set_ylabel('Mean Jaccard index')
ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
ax1.set_ylim(0.3, 0.8)
xtick_names = setp(ax1, xticklabels=t1t2_names)
setp(xtick_names, rotation=45, fontsize=16)

######T1-PD####
t1pd_scores = [cc_t1t1, cc_t1pd, ecc_t1pd, em_t1pd, mi_t1pd]
t1pd_names = ["Baseline", "CC", "ECC", "EM", "MI"]
fig, ax1 = plt.subplots()
boxplot(t1pd_scores)
ax1.set_axisbelow(True)
ax1.set_title('Distribution of mean Jaccard scores (averaged over 31 regions per pair). Registration of 612 T1-PD pairs.')
ax1.set_ylabel('Mean Jaccard index')
ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
ax1.set_ylim(0.3, 0.8)
xtick_names = setp(ax1, xticklabels=t1pd_names)
setp(xtick_names, rotation=45, fontsize=16)

#####T2-PD####
t2pd_scores = [cc_t1t1, cc_t2pd, ecc_t2pd, em_t2pd, mi_t2pd]
t2pd_names = ["Baseline", "CC", "ECC", "EM", "MI"]
fig, ax1 = plt.subplots()
boxplot(t2pd_scores)
ax1.set_axisbelow(True)
ax1.set_title('Distribution of mean Jaccard scores (averaged over 31 regions per pair). Registration of 612 T2-PD pairs.')
ax1.set_ylabel('Mean Jaccard index')
ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
ax1.set_ylim(0.3, 0.8)
xtick_names = setp(ax1, xticklabels=t2pd_names)
setp(xtick_names, rotation=45, fontsize=16)


scores = [[t1t1_scores, t1t2_scores, t1pd_scores], [None, t2t2_scores, t2pd_scores], [None, None, pdpd_scores]]
names = [[t1t1_names, t1t2_names, t1pd_names], [None, t2t2_names, t2pd_names], [None, None, pdpd_names]]
mod_names = ["T1", "T2", "PD"]

figure()
idx = 0;
for i in range(3):
    for j in range(3):
        idx += 1
        if scores[i][j] is None:
            continue
        ax = subplot(3, 3, idx)
        boxplot(scores[i][j][-4:])
        ax.set_axisbelow(True)
        ax.set_title(mod_names[i]+" - "+mod_names[j])
        ax.set_ylabel('Mean Jaccard index')
        ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
        ax.set_ylim(0.3, 0.8)
        xtick_names = setp(ax, xticklabels=names[i][j][-4:])
        setp(xtick_names, fontsize=16)


