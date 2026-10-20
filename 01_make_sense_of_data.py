import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# 1. DATA SIMULATION (Membuat dataset sintetis transaksi faktur PT Maju Bersama)
np.random.seed(42)
n_samples = 1200

data = {
    'invoice_amount': np.random.uniform(1000, 50000, n_samples),
    'credit_score': np.random.randint(300, 850, n_samples),
    'payment_terms_days': np.random.choice([15, 30, 45, 60], n_samples),
    'past_late_payments': np.random.poisson(lam=1.2, size=n_samples),
    'discount_rate': np.random.uniform(0.0, 0.15, n_samples),
    'customer_tenure_months': np.random.randint(1, 60, n_samples)
}

df = pd.DataFrame(data)

# Logika penetapan target variable 'is_late' (1 = Late Payment, 0 = On Time)
logit = (
    - 0.006 * (df['credit_score'] - 600)
    + 0.6 * df['past_late_payments']
    + 0.00005 * df['invoice_amount']
    - 0.03 * df['customer_tenure_months']
    - 1.5
)
prob_late = 1 / (1 + np.exp(-logit))
df['is_late'] = (np.random.binomial(1, prob_late) == 1).astype(int)

# 2. DATA PREPARATION & FEATURE SELECTION
X = df.drop(columns=['is_late'])
y = df['is_late']

# Split Data (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. MODELING (Random Forest Classifier)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4. EVALUATION
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("=== EVALUASI MODEL PREDIKSI LATE PAYMENT ===")
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("ROC AUC Score:", round(roc_auc_score(y_test, y_proba), 4))

# Feature Importance (Diagnostik Fitur Paling Berpengaruh)
importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': model.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("\n=== FITUR PALING MEMPENGARUHI KETERLAMBATAN BAYAR ===")
print(importance.to_string(index=False))