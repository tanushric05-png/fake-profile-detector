import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# -------------------------------
# Step 1: Create Dataset
# -------------------------------
data = {
    'followers': [10, 200, 50, 500, 30, 1000, 20, 800],
    'following': [300, 180, 400, 200, 500, 300, 450, 250],
    'posts': [2, 50, 5, 100, 3, 200, 1, 150],
    'bio_length': [5, 50, 10, 80, 8, 100, 3, 90],
    'fake': [1, 0, 1, 0, 1, 0, 1, 0]   # 1 = Fake, 0 = Real
}

df = pd.DataFrame(data)

# -------------------------------
# Step 2: Features & Label
# -------------------------------
X = df[['followers', 'following', 'posts', 'bio_length']]
y = df['fake']

# -------------------------------
# Step 3: Split Data
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# Step 4: Train Model
# -------------------------------
model = LogisticRegression(max_iter=200)  # increased iterations to avoid warnings
model.fit(X_train, y_train)

# -------------------------------
# Step 5: Accuracy
# -------------------------------
accuracy = model.score(X_test, y_test)
print("Model Accuracy:", round(accuracy * 100, 2), "%")

# -------------------------------
# Step 6: User Input
# -------------------------------
print("\nEnter Profile Details:")

followers = int(input("Followers: "))
following = int(input("Following: "))
posts = int(input("Number of Posts: "))
bio = int(input("Bio Length: "))

# -------------------------------
# Step 7: Prediction
# -------------------------------
new_data = pd.DataFrame([[followers, following, posts, bio]],
                        columns=['followers', 'following', 'posts', 'bio_length'])

result = model.predict(new_data)

print("\nResult:")

if result[0] == 1:
    print("Fake Profile ❌")
else:
    print("Real Profile ✅")