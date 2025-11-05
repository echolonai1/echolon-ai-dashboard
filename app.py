footer_html = f"""<div class=\"neon-footer\">
    <span style=\"font-size:37px;font-weight:bold;color:#00fff7;\">AI-Driven Savings</span><br/><br/>
    <span style=\"font-size:23px;font-family:monospace;letter-spacing:2.5px;\">{savings_amt:,}</span>
</div>"""
st.markdown(footer_html, unsafe_allow_html=True)
