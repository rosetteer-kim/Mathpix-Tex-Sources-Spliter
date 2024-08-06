import streamlit as st
import split_mathpix_tex_source as smts
import modify_latex_scripts.letter_of_choice as ml


def main():
    st.title("Mathpix TeX Source Spliter")

    questions_file = st.file_uploader("TeX File: 반드시 문제", type="tex")
    if questions_file is not None:
        questions = questions_file.getvalue().decode("utf-8")
        if st.button("문제 분리"):
            # tex file 분리
            questions_split = smts.split_mathpix_tex_source(questions)
            # 선지 추출 및 문제 형식(객관식, 주관식) 구별
            mod_loc_q_split = ml.modify_letter_of_choice(questions_split)
            st.write(f"문제 수: {len(questions_split)}")

            st.markdown("---")  # 구분선 추가
            exercises = ""
            # for i, content in enumerate(mod_loc_q_split):
            #     exercises += 'S' + 'ㅡ' * 10 + ' ' + f'{i + 1}번' + ' ' + 'ㅡ' * 10 + '\n'
            #     exercises += content[0]
            #     exercises += 'E' + 'ㅡ' * 10 + ' ' + f'{i + 1}번' + ' ' + 'ㅡ' * 10 + '\n\n\n'
            # txt = st.text_area(f'\n',exercises, height=1000)
            for i, content in enumerate(mod_loc_q_split):
                # txt = st.text_area(f'{'-'*10} {i + 1}번 {'-'*10}', content[0], height=500)
                with st.expander(f"문제 {i + 1}"):
                    st.text(content[0])
                with st.expander(f"형태: {content[2]}"):
                    st.text(content[1])

            st.markdown("---")  # 구분선 추가
    solutions_file = st.file_uploader("TeX File: 해설", type="tex")
    if solutions_file is not None:
        solutions = solutions_file.getvalue().decode("utf-8")
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
        qus_and_sol_file = st.file_uploader("TeX File: 문제와 해설 (개발 전)", type="tex")
        if st.button("문항과 해설 동시 분리"):
            qus_and_sol = qus_and_sol_file.getvalue().decode("utf-8")
            pass

main()