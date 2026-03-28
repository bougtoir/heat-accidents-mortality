"""
Dynamic model + Visualizations using pre-filtered CSVs for speed.
"""
import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
from scipy.stats import norm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, warnings, sys
warnings.filterwarnings('ignore')
os.makedirs('/home/ubuntu/figures', exist_ok=True)

print("Loading pre-filtered data...", flush=True)
demo_f = pd.read_csv('/home/ubuntu/wpp_data/demo_filtered.csv', low_memory=False)
pop_age5 = pd.read_csv('/home/ubuntu/wpp_data/pop_age5_filtered.csv', low_memory=False)
print(f"Demo: {demo_f.shape}, PopAge5: {pop_age5.shape}", flush=True)

country_ids = {
    "Australia":36,"Austria":40,"Belgium":56,"Canada":124,"Chile":152,
    "China":156,"Colombia":170,"Costa Rica":188,"Czechia":203,
    "DRC":180,"Denmark":208,"Estonia":233,"Finland":246,"France":250,
    "Germany":276,"Greece":300,"Hungary":348,"Iceland":352,
    "Ireland":372,"Israel":376,"Italy":380,"Japan":392,
    "Republic of Korea":410,"Latvia":428,"Lithuania":440,"Luxembourg":442,
    "Mexico":484,"Netherlands":528,"New Zealand":554,"Norway":578,
    "Poland":616,"Portugal":620,"Slovakia":703,"Slovenia":705,
    "Spain":724,"Sweden":752,"Switzerland":756,"Türkiye":792,
    "United Kingdom":826,"United States":840
}
id_to_name = {v:k for k,v in country_ids.items()}

# Model functions
def gompertz_survival(x, a_g, b_g):
    x = np.asarray(x, dtype=float)
    return np.exp(-(a_g/b_g)*np.expm1(b_g*x))

def calibrate_gompertz(target_le, b_g=0.085):
    def obj(log_a):
        a = np.exp(log_a)
        ages = np.arange(0, 111, dtype=float)
        return (np.trapezoid(gompertz_survival(ages, a, b_g), ages) - target_le)**2
    res = minimize_scalar(obj, bounds=(-14,-1), method='bounded')
    return np.exp(res.x), b_g

def make_asfr(mac, sigma, tfr, max_age=100):
    asfr = np.zeros(max_age+1)
    fertile = np.arange(15,50)
    pdf = norm.pdf(fertile, loc=mac, scale=sigma)
    t = pdf.sum()
    if t > 0: asfr[15:50] = pdf*(tfr/t)
    return asfr

def get_init_pop(loc_id, year, max_age=100):
    sub = pop_age5[(pop_age5['LocID']==loc_id)&(pop_age5['Time']==year)]
    if len(sub)==0: return None
    pop0 = np.zeros(max_age+1)
    for _,r in sub.iterrows():
        grp = str(r['AgeGrp'])
        val = float(r['PopTotal'])*1000
        if '-' in grp:
            parts = grp.split('-')
            a_s,a_e = int(parts[0]),int(parts[1])
            for a in range(a_s, min(a_e+1, max_age+1)):
                pop0[a] = val/(a_e-a_s+1)
        elif '+' in grp:
            a_s = int(grp.replace('+',''))
            pop0[min(a_s,max_age)] += val
    return pop0

def get_sigma(tfr):
    if tfr>4: return 6.5
    elif tfr>2.5: return 5.5
    elif tfr<1.5: return 4.5
    return 5.0

def make_params(loc_id, year):
    row = demo_f[(demo_f['LocID']==loc_id)&(demo_f['Time']==year)]
    if len(row)==0:
        for dy in range(-2,3):
            row = demo_f[(demo_f['LocID']==loc_id)&(demo_f['Time']==year+dy)]
            if len(row)>0: break
    if len(row)==0: return None
    row = row.iloc[0]
    tfr=float(row['TFR']); le=float(row['LEx']); mac=float(row['MAC'])
    fem = float(row['TPopulationFemale1July'])/float(row['TPopulation1July']) if row['TPopulation1July']>0 else 0.5
    sigma = get_sigma(tfr)
    a_g,b_g = calibrate_gompertz(le)
    surv_arr = gompertz_survival(np.arange(0,102,dtype=float), a_g, b_g)
    asfr = make_asfr(mac, sigma, tfr)
    sr = np.zeros(101)
    for a in range(1,101):
        sr[a] = min(1.0, max(0.0, surv_arr[a]/surv_arr[a-1])) if surv_arr[a-1]>1e-15 else 0
    inf_surv = min(1.0, surv_arr[1]/surv_arr[0]) if surv_arr[0]>1e-15 else 0.95
    return {'asfr':asfr,'sr':sr,'inf_surv':inf_surv,'fem':fem,'tfr':tfr,'le':le,'mac':mac}

def run_dynamic(loc_id, start=1970, end=2023):
    pop0 = get_init_pop(loc_id, start)
    if pop0 is None: return None, None
    n = end-start; pop = np.zeros((n+1,101)); pop[0]=pop0
    total = np.zeros(n+1); total[0]=pop0.sum()
    cache = {}
    for t in range(1,n+1):
        py = start+((t-1)//10)*10
        if py not in cache:
            p = make_params(loc_id, py)
            if p is None: break
            cache[py] = p
        p = cache[py]
        births = np.sum(pop[t-1,15:50]*p['fem']*p['asfr'][15:50])
        pop[t,1:] = pop[t-1,:-1]*p['sr'][1:]
        pop[t,0] = max(0, births*p['inf_surv'])
        total[t] = pop[t].sum()
    return np.arange(start, start+n+1), total

def run_static(loc_id, start=1970, end=2023):
    pop0 = get_init_pop(loc_id, start)
    if pop0 is None: return None, None
    p = make_params(loc_id, start)
    if p is None: return None, None
    n = end-start; pop = np.zeros((n+1,101)); pop[0]=pop0
    total = np.zeros(n+1); total[0]=pop0.sum()
    for t in range(1,n+1):
        births = np.sum(pop[t-1,15:50]*p['fem']*p['asfr'][15:50])
        pop[t,1:] = pop[t-1,:-1]*p['sr'][1:]
        pop[t,0] = max(0, births*p['inf_surv'])
        total[t] = pop[t].sum()
    return np.arange(start, start+n+1), total

def calc_metrics(yrs, pops, actual_years, actual_pop):
    common = np.intersect1d(yrs, actual_years)
    if len(common)<5: return None
    mv = np.array([pops[np.where(yrs==y)[0][0]] for y in common])
    av = np.array([actual_pop[np.where(actual_years==y)[0][0]] for y in common])
    if av[0]==0: return None
    mi=mv/mv[0]; ai=av/av[0]
    mape = np.mean(np.abs((mi-ai)/ai))*100
    mape_abs = np.mean(np.abs((mv-av)/av))*100
    ratio = mv[-1]/av[-1] if av[-1]>0 else np.nan
    return {'mape_index':mape,'mape_abs':mape_abs,'final_ratio':ratio}

# Run all
print("\nRunning models for all 40 countries...", flush=True)
START=1970; END=2023
all_r = {}; dyn_res=[]; stat_res=[]

for cn, lid in sorted(country_ids.items()):
    sub = demo_f[(demo_f['LocID']==lid)&(demo_f['Time']>=START)&(demo_f['Time']<=END)].sort_values('Time')
    ay = sub['Time'].values; ap = sub['TPopulation1July'].values*1000
    dy, dp = run_dynamic(lid, START, END)
    sy, sp = run_static(lid, START, END)
    all_r[cn] = {'ay':ay,'ap':ap,'dy':dy,'dp':dp,'sy':sy,'sp':sp}
    
    if dy is not None:
        m = calc_metrics(dy,dp,ay,ap)
        if m: dyn_res.append({**m,'country':cn})
    if sy is not None:
        m = calc_metrics(sy,sp,ay,ap)
        if m: stat_res.append({**m,'country':cn})
    print(f"  {cn}: done", flush=True)

dyn_df = pd.DataFrame(dyn_res)
stat_df = pd.DataFrame(stat_res)
print(f"\nDynamic: N={len(dyn_df)}, MAPE mean={dyn_df['mape_index'].mean():.1f}% med={dyn_df['mape_index'].median():.1f}%", flush=True)
print(f"Static:  N={len(stat_df)}, MAPE mean={stat_df['mape_index'].mean():.1f}% med={stat_df['mape_index'].median():.1f}%", flush=True)

# ===== VISUALIZATIONS =====
print("\nGenerating figures...", flush=True)

# Fig 1: 6-panel showcase
showcase = ["Japan","China","United States","Republic of Korea","Germany","DRC"]
fig, axes = plt.subplots(2,3,figsize=(18,10))
for i,cn in enumerate(showcase):
    ax=axes.flatten()[i]; r=all_r[cn]
    ax.plot(r['ay'],r['ap']/1e6,'k-',lw=2,label='UN WPP 2024')
    if r['dy'] is not None: ax.plot(r['dy'],r['dp']/1e6,'b--',lw=1.5,label='Dynamic (10yr)')
    if r['sy'] is not None: ax.plot(r['sy'],r['sp']/1e6,'r:',lw=1.5,label='Static (1970)')
    ax.set_title(cn,fontsize=14,fontweight='bold')
    ax.set_xlabel('Year'); ax.set_ylabel('Pop (M)'); ax.legend(fontsize=8); ax.grid(True,alpha=0.3)
plt.suptitle('Endogenous Renewal + Gompertz vs UN WPP 2024 (1970-2023)',fontsize=16,fontweight='bold')
plt.tight_layout(); plt.savefig('/home/ubuntu/figures/fig1_showcase.png',dpi=150,bbox_inches='tight'); plt.close()
print("  Fig1 done", flush=True)

# Fig 2: All 40 countries
fig, axes = plt.subplots(8,5,figsize=(25,32)); af=axes.flatten()
for i,cn in enumerate(sorted(country_ids.keys())):
    if i>=40: break
    ax=af[i]; r=all_r[cn]
    ax.plot(r['ay'],r['ap']/1e6,'k-',lw=1.5)
    if r['dy'] is not None: ax.plot(r['dy'],r['dp']/1e6,'b--',lw=1)
    if r['sy'] is not None: ax.plot(r['sy'],r['sp']/1e6,'r:',lw=1)
    dr=dyn_df[dyn_df['country']==cn]
    if len(dr)>0:
        ax.text(0.95,0.95,f'MAPE={dr.iloc[0]["mape_index"]:.1f}%',transform=ax.transAxes,fontsize=7,va='top',ha='right',
                bbox=dict(boxstyle='round,pad=0.2',facecolor='lightyellow',alpha=0.8))
    ax.set_title(cn,fontsize=9,fontweight='bold'); ax.tick_params(labelsize=7); ax.grid(True,alpha=0.2)
plt.suptitle('All Countries: Dynamic(blue) Static(red) vs Actual(black) 1970-2023',fontsize=14,fontweight='bold')
plt.tight_layout(); plt.savefig('/home/ubuntu/figures/fig2_all_countries.png',dpi=120,bbox_inches='tight'); plt.close()
print("  Fig2 done", flush=True)

# Fig 3: MAPE heatmap from static results CSV
static_csv = pd.read_csv('/home/ubuntu/model_fit_results.csv')
pivot = static_csv.pivot_table(values='mape_index',index='country',columns='base_year')
fig,ax = plt.subplots(figsize=(10,16))
im = ax.imshow(pivot.values,cmap='RdYlGn_r',aspect='auto',vmin=0,vmax=30)
ax.set_xticks(range(len(pivot.columns))); ax.set_xticklabels([int(c) for c in pivot.columns])
ax.set_yticks(range(len(pivot.index))); ax.set_yticklabels(pivot.index,fontsize=9)
for i in range(len(pivot.index)):
    for j in range(len(pivot.columns)):
        v=pivot.values[i,j]
        if not np.isnan(v):
            ax.text(j,i,f'{v:.1f}',ha='center',va='center',fontsize=7,color='white' if v>20 else 'black')
plt.colorbar(im,ax=ax,label='MAPE (%)',shrink=0.8)
ax.set_title('Static Model MAPE (%) by Country x Base Year',fontsize=14,fontweight='bold')
ax.set_xlabel('Base Year')
plt.tight_layout(); plt.savefig('/home/ubuntu/figures/fig3_heatmap.png',dpi=150,bbox_inches='tight'); plt.close()
print("  Fig3 done", flush=True)

# Fig 4: Dynamic vs Static bar chart
merged = dyn_df.merge(stat_df,on='country',suffixes=('_dyn','_stat'))
fig,(ax1,ax2) = plt.subplots(1,2,figsize=(20,10))
ms = merged.sort_values('mape_index_dyn'); x=np.arange(len(ms)); w=0.35
ax1.barh(x-w/2,ms['mape_index_stat'],w,label='Static(1970)',color='salmon',alpha=0.8)
ax1.barh(x+w/2,ms['mape_index_dyn'],w,label='Dynamic(10yr)',color='steelblue',alpha=0.8)
ax1.set_yticks(x); ax1.set_yticklabels(ms['country'],fontsize=8)
ax1.set_xlabel('MAPE (%)'); ax1.set_title('MAPE: Static vs Dynamic',fontweight='bold')
ax1.legend(); ax1.grid(True,alpha=0.3,axis='x')
ax2.scatter(ms['final_ratio_stat'],ms['final_ratio_dyn'],s=60,alpha=0.7,c='steelblue',edgecolors='black',lw=0.5)
ax2.axhline(1,color='gray',ls='--',alpha=0.5); ax2.axvline(1,color='gray',ls='--',alpha=0.5)
ax2.plot([0.4,3],[0.4,3],'k:',alpha=0.3)
for _,r in ms.iterrows(): ax2.annotate(r['country'],(r['final_ratio_stat'],r['final_ratio_dyn']),fontsize=6,alpha=0.7)
ax2.set_xlabel('Static: Final Ratio'); ax2.set_ylabel('Dynamic: Final Ratio')
ax2.set_title('Final Pop Ratio 2023',fontweight='bold'); ax2.grid(True,alpha=0.3)
plt.tight_layout(); plt.savefig('/home/ubuntu/figures/fig4_comparison.png',dpi=150,bbox_inches='tight'); plt.close()
print("  Fig4 done", flush=True)

# Fig 5: Bias analysis
fig,axes = plt.subplots(1,3,figsize=(18,6))
s2k = static_csv[static_csv['base_year']==2000]
for ax,col,color,title in [(axes[0],'tfr','steelblue','(A) Fit vs TFR'),
                            (axes[1],'le','coral','(B) Fit vs LE'),
                            (axes[2],'mac','forestgreen','(C) Bias vs MAC')]:
    ycol = 'mape_index' if 'Fit' in title else 'final_ratio'
    for _,r in s2k.iterrows():
        ax.scatter(r[col],r[ycol],s=40,alpha=0.7,c=color,edgecolors='black',lw=0.5)
        ax.annotate(r['country'][:3],(r[col],r[ycol]),fontsize=6,alpha=0.6)
    ax.set_xlabel(f'{col.upper()} (2000)'); ax.set_ylabel('MAPE (%)' if 'Fit' in title else 'Final Ratio')
    ax.set_title(title,fontweight='bold'); ax.grid(True,alpha=0.3)
    if 'Bias' in title: ax.axhline(1,color='gray',ls='--',alpha=0.5)
plt.suptitle('Model Bias Analysis (Base Year=2000)',fontsize=14,fontweight='bold')
plt.tight_layout(); plt.savefig('/home/ubuntu/figures/fig5_bias.png',dpi=150,bbox_inches='tight'); plt.close()
print("  Fig5 done", flush=True)

# Save summaries
dyn_df.to_csv('/home/ubuntu/model_fit_dynamic_results.csv',index=False)
summary = []
for by in [1970,1980,1990,2000]:
    sub=static_csv[static_csv['base_year']==by]
    if len(sub)==0: continue
    summary.append({'Base Year':by,'Horizon':int(sub['horizon'].median()),'N':len(sub),
        'MAPE Mean':f"{sub['mape_index'].mean():.1f}",'MAPE Median':f"{sub['mape_index'].median():.1f}",
        'Ratio Mean':f"{sub['final_ratio'].mean():.3f}",'Ratio Std':f"{sub['final_ratio'].std():.3f}"})
summary.append({'Base Year':'1970(dyn)','Horizon':53,'N':len(dyn_df),
    'MAPE Mean':f"{dyn_df['mape_index'].mean():.1f}",'MAPE Median':f"{dyn_df['mape_index'].median():.1f}",
    'Ratio Mean':f"{dyn_df['final_ratio'].mean():.3f}",'Ratio Std':f"{dyn_df['final_ratio'].std():.3f}"})
pd.DataFrame(summary).to_csv('/home/ubuntu/model_fit_summary.csv',index=False)

print("\n" + "="*60, flush=True)
print("DYNAMIC MODEL RESULTS (sorted by MAPE)", flush=True)
print("="*60, flush=True)
for _,r in dyn_df.sort_values('mape_index').iterrows():
    print(f"  {r['country']:25s} MAPE={r['mape_index']:6.1f}%  ratio={r['final_ratio']:.3f}", flush=True)

print("\nAll done!", flush=True)
