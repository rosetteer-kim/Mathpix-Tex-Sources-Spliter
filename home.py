import streamlit as st
import split_mathpix_tex_source as smts


def main():
    st.title("Mathpix TeX Source Spliter")

    questions_file = st.file_uploader("TeX File: 문제", type="tex")
    solutions_file = st.file_uploader("TeX File: 해설", type="tex")
    if questions_file is not None and solutions_file is not None:
        questions = questions_file.getvalue().decode("utf-8")
        solutions = solutions_file.getvalue().decode("utf-8")
        if st.button("Mathpix Tex sources 분리"):
            # tex file 분리
            questions_split = smts.split_mathpix_tex_source(questions)
            solutions_split = smts.split_mathpix_tex_source(solutions)

            st.write(f"문제 수: {len(questions_split)}, 해설 수: {len(solutions_split)}")

            st.markdown("---")  # 구분선 추가
            for i, content in enumerate(questions_split):
                with st.expander(f"문제 {i+1}"):
                    st.text(content)
            st.markdown("---")  # 구분선 추가
            for i, content in enumerate(solutions_split):
                with st.expander(f"해설 {i+1}"):
                    st.text(content)
            st.markdown("---")  # 구분선 추가

main()