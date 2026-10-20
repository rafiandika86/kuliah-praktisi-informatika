import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    # 1. SIMULASI DATASET INTERAKSI PENGGUNA (HCI / UI-UX EXPERIMENT DATA)
    np.random.seed(42)
    n_users = 200

    versions = np.random.choice(['UI_V1_Baseline', 'UI_V2_Redesign'], size=n_users, p=[0.5, 0.5])

    completion_time = []
    error_count = []
    sus_score = []

    for v in versions:
        if v == 'UI_V1_Baseline':
            completion_time.append(np.random.normal(loc=140, scale=25))
            error_count.append(np.random.poisson(lam=3.2))
            sus_score.append(np.random.normal(loc=62, scale=12))
        else:
            completion_time.append(np.random.normal(loc=95, scale=18))
            error_count.append(np.random.poisson(lam=1.1))
            sus_score.append(np.random.normal(loc=82, scale=9))

    df = pd.DataFrame({
        'user_id': [f"USR_{i:03d}" for i in range(1, n_users + 1)],
        'interface_version': versions,
        'task_time_sec': np.clip(completion_time, 30, 300),
        'error_count': error_count,
        'sus_score': np.clip(sus_score, 0, 100)
    })

    # 2. PROSES AGREGASI & DATA ANALYSIS
    summary = df.groupby('interface_version').agg(
        avg_time_sec=('task_time_sec', 'mean'),
        avg_errors=('error_count', 'mean'),
        avg_sus_score=('sus_score', 'mean')
    ).reset_index()

    print("=== DATA SUMMARY METRIK HCI & USABILITY EVALUATION ===")
    print(summary.round(2).to_string(index=False))

    # 3. VISUALISASI DATA (MULTILAYER DASHBOARD SETUP)
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Plot 1: Waktu Penyelesaian Tugas
    sns.boxplot(ax=axes[0], data=df, x='interface_version', y='task_time_sec', palette='Set2')
    axes[0].set_title("Waktu Penyelesaian Tugas (detik)", fontsize=12, fontweight='bold')
    axes[0].set_xlabel("Versi Antarmuka")
    axes[0].set_ylabel("Waktu (Detik)")

    # Plot 2: Jumlah Error
    sns.barplot(ax=axes[1], data=df, x='interface_version', y='error_count', palette='Set2', errorbar=None)
    axes[1].set_title("Rata-rata Jumlah Error Pengguna", fontsize=12, fontweight='bold')
    axes[1].set_xlabel("Versi Antarmuka")
    axes[1].set_ylabel("Rata-rata Error")

    # Plot 3: Skor Usability (SUS)
    sns.kdeplot(ax=axes[2], data=df, x='sus_score', hue='interface_version', fill=True, palette='Set2')
    axes[2].set_title("Distribusi Skor System Usability Scale (SUS)", fontsize=12, fontweight='bold')
    axes[2].set_xlabel("Skor SUS")
    axes[2].set_ylabel("Kepadatan (Density)")

    plt.tight_layout()
    plt.savefig("hci_usability_dashboard.png")
    print("\nDashboard visualisasi berhasil dibuat dan disimpan sebagai 'hci_usability_dashboard.png'.")

if __name__ == "__main__":
    main()