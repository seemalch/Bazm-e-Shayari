import streamlit as st
import numpy as np
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Clear any existing TensorFlow sessions to avoid conflicts
tf.keras.backend.clear_session()

# Try loading the model with compatibility mode in case of version issues
try:
    # Load the model
    model = tf.keras.models.load_model("poetry_generator.h5")
except:
    # If loading fails, use tf.compat.v1 for legacy support
    model = tf.compat.v1.keras.models.load_model("poetry_generator.h5")

# Load tokenizer
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Define the sample function for temperature sampling
def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    return np.random.choice(len(preds), p=preds)

# Define the text generation function
def generate_text(seed_text, model, tokenizer, max_seq_length, temperature=1.0, num_lines=1, words_per_line=5):
    generated_text = ""
    for _ in range(num_lines):  # Generate specified number of lines
        line = seed_text
        for _ in range(words_per_line):  # Generate words for each line
            token_list = tokenizer.texts_to_sequences([line])[0]
            token_list = pad_sequences([token_list], maxlen=max_seq_length-1, padding='pre')
            preds = model.predict(token_list, verbose=0)
            next_word_idx = sample(preds[0], temperature)
            next_word = tokenizer.index_word[next_word_idx]
            line += " " + next_word
        generated_text += line + "<br>"  # Use <br> for line break in HTML
    return generated_text

# Streamlit app UI
st.set_page_config(page_title="Bazm-e-Shayari", page_icon="🎤", layout="wide")

# Header with Emoji
st.title("🎤 **Bazm-e-Shayari** 🎶")
st.write("Generate beautiful Roman Urdu poetry with a touch of creativity! ✨")

# User Inputs Section with Emojis and Icons
st.sidebar.header("Input Settings 🌟")
seed_text = st.sidebar.text_input("Enter the seed text 🌱:", placeholder="E.g. dil ki baat...")
num_lines = st.sidebar.slider("Select the number of lines to generate 📜", 1, 10, 1)
words_per_line = st.sidebar.slider("Select the number of words per line 📝", 1, 10, 5)
temperature = st.sidebar.slider("Select the creativity (temperature) 🎨", 0.1, 2.0, 0.8, step=0.1)

# Add a Loading Spinner to indicate text generation
with st.spinner('Generating poetry... ⏳'):
    if st.sidebar.button("Generate Poetry 📜"):
        if seed_text:
            # Get the maximum sequence length from the model
            max_seq_length = model.input_shape[1]

            # Generate the text
            generated_text = generate_text(seed_text, model, tokenizer, max_seq_length, temperature, num_lines, words_per_line)

            # Display the generated text with line breaks
            st.subheader("Generated Poetry 💬:")
            st.markdown(generated_text, unsafe_allow_html=True)  # Render HTML with <br> for line breaks
        else:
            st.error("Please enter a seed text to generate poetry. ⚠️")

# Footer Section with Emoji and GitHub Profile Link
st.markdown("""
    <style>
        .footer {
            text-align: center;
            padding: 10px;
            font-size: 14px;
            color: #808080;
        }
        .footer a {
            color: #0366d6;
            text-decoration: none;
        }
        .footer a:hover {
            color: #0366d6;
        }
    </style>
    <div class="footer">
        <p>💡 Poetry generated by Bazm-e-Shayari. Powered by AI ✨</p>
        <p>Visit my GitHub: <a href="https://github.com/seemalch" target="_blank">GitHub Profile</a></p>
    </div>
""", unsafe_allow_html=True)

