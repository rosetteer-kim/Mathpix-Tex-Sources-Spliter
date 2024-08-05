import streamlit as st
import split_mathpix_tex_source as smts
import modify_latex_scripts.letter_of_choice as ml


def main():
    st.title("Mathpix TeX Source Spliter")

    questions_file = st.file_uploader("TeX File: 반드시 문제", type="tex")
    solutions_file = st.file_uploader("TeX File: 해설", type="tex")
    if questions_file is not None and solutions_file is not None:
        questions = questions_file.getvalue().decode("utf-8")
        solutions = solutions_file.getvalue().decode("utf-8")
        if st.button("문제 분리"):
            # tex file 분리
            questions_split = smts.split_mathpix_tex_source(questions)
            # 선지 추출 및 문제 형식(객관식, 주관식) 구별
            mod_loc_q_split = ml.modify_letter_of_choice(questions_split)
            st.write(f"문제 수: {len(questions_split)}")

            st.markdown("---")  # 구분선 추가

            for i, content in enumerate(mod_loc_q_split):
                with st.expander(f"문제 {i + 1}"):
                    st.text(content[0])
                with st.expander(f"형태: {content[2]}"):
                    st.text(content[1])

            st.markdown("---")  # 구분선 추가
        if st.button("해설 분리"):
            # tex file 분리
            solutions_split = smts.split_mathpix_tex_source(solutions)
            # 선지 추출 및 문제 형식(객관식, 주관식) 구별

            st.write(f"해설 수: {len(solutions_split)}")

            st.markdown("---")  # 구분선 추가

            for i, content in enumerate(solutions_split):
                with st.expander(f"해설 {i+1}"):
                    st.text(content)
            st.markdown("---")  # 구분선 추가
        if st.button("문항과 해설 동시 분리"):
            pass

main()