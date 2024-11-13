import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split 
import seaborn as sns
from matplotlib.colors import ListedColormap
from sklearn.preprocessing import LabelEncoder

dataset = sns.load_dataset('iris')
print(dataset)


# Step 1: Sigmoid Function
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# Step 2: Prediction Function
def predict(X, weights):
    z = np.dot(X, weights)
    return sigmoid(z)

# Step 3: Loss Function (Binary Cross-Entropy)
def compute_loss(y, y_pred):
    return -np.mean(y * np.log(y_pred) + (1 - y) * np.log(1 - y_pred))

# Step 4: Gradient Descent
def gradient_descent(X, y, weights, learning_rate):
    N = len(y)
    y_pred = predict(X, weights)
    gradient = np.dot(X.T, (y_pred - y)) / N
    weights -= learning_rate * gradient
    return weights

# Step 5: Training Function
def train_logistic_regression(X, y, learning_rate=0.01, epochs=1000):
    # Initialize weights
    weights = np.zeros(X.shape[1])

    # Gradient Descent
    for epoch in range(epochs):
        y_pred = predict(X, weights)
        loss = compute_loss(y, y_pred)
        weights = gradient_descent(X, y, weights, learning_rate)

        # Print the loss every 100 epochs for tracking
        if epoch % 100 == 0:
            print(f'aEpoch {epoch}: Loss = {loss}')

    return weights


# Prepare the features and target variable
X = dataset[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']].values
y = dataset['species'].values

# Convert categorical labels to numeric values
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)  # This converts species names to integers

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.3, random_state=42)

# Add bias term to training and testing data
X_train_with_bias = np.hstack((np.ones((X_train.shape[0], 1)), X_train))  # Add a column of ones for bias
X_test_with_bias = np.hstack((np.ones((X_test.shape[0], 1)), X_test))  # Add a column of ones for bias

# Training function and other required functions (assuming these are already defined)
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def predict(X, weights):
    z = np.dot(X, weights)
    return sigmoid(z)

def compute_loss(y, y_pred):
    return -np.mean(y * np.log(y_pred + 1e-15) + (1 - y) * np.log(1 - y_pred + 1e-15))  # Adding epsilon to prevent log(0)

def gradient_descent(X, y, weights, learning_rate):
    N = len(y)
    y_pred = predict(X, weights)
    gradient = np.dot(X.T, (y_pred - y)) / N
    weights -= learning_rate * gradient
    return weights

def train_logistic_regression(X, y, learning_rate=0.01, epochs=1000):
    # Initialize weights
    weights = np.zeros(X.shape[1])
    
    # Gradient Descent
    for epoch in range(epochs):
        y_pred = predict(X, weights)
        loss = compute_loss(y, y_pred)
        weights = gradient_descent(X, y, weights, learning_rate)

        # Print the loss every 100 epochs for tracking
        if epoch % 100 == 0:
            print(f'Epoch {epoch}: Loss = {loss}')

    return weights

# Train the model on training data
weights = train_logistic_regression(X_train_with_bias, y_train, learning_rate=0.1, epochs=1000)
print("Trained weights:", weights)
print("Trained weights:", weights)

# Color maps
cm = plt.cm.Blues
cm_bright = ListedColormap(['#FFFF00', '#00FFFF'])

# Plotting setup
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Step 1: Training and Testing Data Points
axes[0].set_title("Training and Testing Data Points")
axes[0].scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright, edgecolors='k', label="Training")
axes[0].scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright, alpha=0.6, edgecolors='k', label="Testing")
axes[0].legend()
axes[0].set_xticks(()); axes[0].set_yticks(())

# Discretize the plot area
h = .02
x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# Step 2: Decision Boundary with Probability Heatmap
X_plot = np.c_[np.ones((xx.ravel().shape[0], 1)), xx.ravel()]
Z = predict(X_plot, weights).reshape(xx.shape)

axes[1].contourf(xx, yy, Z, cmap=cm, alpha=0.65)
axes[1].scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright, edgecolors='k')
axes[1].scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright, edgecolors='k', alpha=0.1)
axes[1].set_xticks(()); axes[1].set_yticks(())

# Step 3: Rounded Decision Boundary
axes[2].set_title("Rounded Decision Boundary")
axes[2].scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright, edgecolors='k')
axes[2].scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright, edgecolors='k', alpha=0.1)
axes[2].contourf(xx, yy, np.round(Z), cmap=cm, alpha=0.65)
axes[2].set_xticks(()); axes[2].set_yticks(())

# Show plot
plt.tight_layout()
plt.show()