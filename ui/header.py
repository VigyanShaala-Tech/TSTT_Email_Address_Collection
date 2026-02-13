import streamlit as st

# Display the PNG image in the top centre of the Streamlit sidebar with custom dimensions

def header():
    st.markdown("""
        <style>
        .status-box {
            padding: 0.75rem 1rem;
            border-radius: 8px;
            font-weight: bold;
            font-size: 1.2rem;
            display: inline-block;
            margin-top: 0.5rem;
            border: 1px solid transparent;
        }

        .status-red {
            background-color: #660000;
            border-color: #cc0000;
            color: #ffcccc;
                font-size: 1.5rem;
        }
        .status-green {
            background-color: #69AB4A;
            border-color: #00cc66;
            color: #000000;
            font-size: 1.5rem;
        }
        .status-orange {
            background-color: #F79630;
            border-color: #ffaa00;
            color: #000000;
            font-size: 1.5rem;
        }
        .status-pink {
            background-color: #FFCC29;
            border-color: #ffccce6;
            color: #000000;
            font-size: 1.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

    co1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.image(r"C:\Vigyanshala\03 run_scripts\TSTT_Email_Address_Collection\TSTT_Email_Address_Collection\ui\log.png", width=200)


    # Display the title of the Google form
    st.markdown(
        "<h1 style='color: black; font-weight: bold; font-size: 2.5rem;'>Email Address Collection</h1>", 
        unsafe_allow_html=True)