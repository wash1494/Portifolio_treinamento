import streamlit as st
import pandas as pd
import os
from PIL import Image
from datetime import datetime
import io
import shutil

# Configure page - DEVE SER O PRIMEIRO COMANDO STREAMLIT
st.set_page_config(page_title="Training Portfolio", layout="wide")

# Default image configuration
DEFAULT_IMAGE = "c:\\WCD\\APP PROGRAMING\\FORMULARIOS DE INVITE\\images\\default_course.png"
if not os.path.exists(DEFAULT_IMAGE):
    img = Image.new('RGB', (400, 300), color='gray')
    img.save(DEFAULT_IMAGE)

# Modificar a função get_course_image para redimensionar as imagens
def get_course_image(image_path):
    try:
        if os.path.exists(image_path):
            # Abrir a imagem e redimensionar para um tamanho padrão
            img = Image.open(image_path)
            # Definir tamanho padrão (proporções semelhantes ao card do NR 06)
            img = img.resize((400, 300), Image.LANCZOS)
            
            # Criar um arquivo temporário para a imagem redimensionada
            temp_path = os.path.join(IMAGES_DIR, "temp_" + os.path.basename(image_path))
            img.save(temp_path)
            return temp_path
        return DEFAULT_IMAGE
    except Exception:
        return DEFAULT_IMAGE

# Initialize session state
if 'current_course' not in st.session_state:
    st.session_state.current_course = None

# File paths
COURSES_DB = "c:\\WCD\\APP PROGRAMING\\FORMULARIOS DE INVITE\\courses.xlsx"
REGISTRATIONS_DB = "c:\\WCD\\APP PROGRAMING\\FORMULARIOS DE INVITE\\registrations.xlsx"
IMAGES_DIR = "c:\\WCD\\APP PROGRAMING\\FORMULARIOS DE INVITE\\images"

# Create images directory if it doesn't exist
os.makedirs(IMAGES_DIR, exist_ok=True)

# No início do arquivo, após carregar as bibliotecas, adicione esta função de limpeza
def clean_invalid_courses():
    df = pd.read_excel(COURSES_DB)
    invalid_courses = []
    
    for idx, course in df.iterrows():
        if not os.path.exists(course['image_path']):
            invalid_courses.append(idx)
    
    if invalid_courses:
        df = df.drop(invalid_courses)
        df.to_excel(COURSES_DB, index=False)
        return True
    return False

# Logo após a definição de IMAGES_DIR, adicione:
# Limpar cursos com imagens inválidas
if os.path.exists(COURSES_DB):
    if clean_invalid_courses():
        st.warning("Alguns cursos com imagens inválidas foram removidos.")

def migrate_courses_db():
    if os.path.exists(COURSES_DB):
        df = pd.read_excel(COURSES_DB)
        if 'status' not in df.columns:
            df['status'] = 'open'  # Set default status for existing courses
            df.to_excel(COURSES_DB, index=False)
        return df
    return pd.DataFrame(columns=['name', 'description', 'slots', 'image_path', 'registered', 'status'])

# Replace the existing load_or_create_courses_db function with:
def load_or_create_courses_db():
    return migrate_courses_db()

def save_course(name, description, slots, image_file):
    df = load_or_create_courses_db()
    
    # Save image to file
    image_path = os.path.join(IMAGES_DIR, f"{name.replace(' ', '_')}.png")
    with open(image_path, 'wb') as f:
        f.write(image_file)
    
    new_course = {
        'name': name,
        'description': description,
        'slots': slots,
        'image_path': image_path,
        'registered': 0,
        'status': 'open'  # Default status for new courses
    }
    df = pd.concat([df, pd.DataFrame([new_course])], ignore_index=True)
    df.to_excel(COURSES_DB, index=False)

def load_or_create_registrations_db():
    if os.path.exists(REGISTRATIONS_DB):
        return pd.read_excel(REGISTRATIONS_DB)
    return pd.DataFrame(columns=['course_name', 'name', 'cpf', 'email', 'company', 'registration_date'])

def save_registration(course_name, name, cpf, email, company):
    df = load_or_create_registrations_db()
    new_registration = {
        'course_name': course_name,
        'name': name,
        'cpf': cpf,
        'email': email,
        'company': company,
        'registration_date': datetime.now()
    }
    df = pd.concat([df, pd.DataFrame([new_registration])], ignore_index=True)
    df.to_excel(REGISTRATIONS_DB, index=False)
    
    # Update course registration count
    courses_df = load_or_create_courses_db()
    courses_df.loc[courses_df['name'] == course_name, 'registered'] += 1
    courses_df.to_excel(COURSES_DB, index=False)

# Ajustar a seção do menu de navegação
st.sidebar.title("Navigation")

# Botão para a Biblioteca
if st.sidebar.button("Library", use_container_width=True):
    st.session_state.page = "Library"
    # Forçar recarregamento para garantir que a autenticação seja verificada
    st.rerun()

# Seção de Management com autenticação única
with st.sidebar.expander("Management"):
    # Verificar autenticação para a área administrativa
    if 'authenticated_admin_area' not in st.session_state:
        st.session_state.authenticated_admin_area = False
    
    if not st.session_state.authenticated_admin_area:
        with st.form("auth_form_admin_area"):
            password = st.text_input("Enter admin password", type="password")
            if st.form_submit_button("Login"):
                if password == "ADMINIDG2025":
                    st.session_state.authenticated_admin_area = True
                    st.rerun()
                else:
                    st.error("Incorrect password")
    else:
        # Botões para as seções administrativas
        if st.button("Course Management", key="btn_course_mgmt", use_container_width=True):
            st.session_state.page = "Course Management"
            st.rerun()
        
        if st.button("Admin Dashboard", key="btn_admin_dash", use_container_width=True):
            st.session_state.page = "Admin Dashboard"
            st.rerun()

# Inicializar a página padrão se não existir
if 'page' not in st.session_state:
    st.session_state.page = "Library"

# Usar st.session_state.page em vez de page
page = st.session_state.page

# Manter a autenticação da biblioteca
if 'authenticated_library' not in st.session_state:
    st.session_state.authenticated_library = False

# Agora vamos ajustar as seções de conteúdo para garantir que funcionem corretamente

# Modificar a seção da Library para manter a autenticação
if page == "Library":
    if not st.session_state.authenticated_library:
        with st.form("auth_form"):
            password = st.text_input("Enter password", type="password")
            if st.form_submit_button("Login"):
                if password == "IDG2025":
                    st.session_state.authenticated_library = True
                    st.rerun()
                else:
                    st.error("Incorrect password")
    else:
        st.title("Training Library")
        # Filter only open courses
        courses_df = load_or_create_courses_db()
        active_courses_df = courses_df[courses_df['status'] == 'open']
        
        # Na seção da Library, onde os cursos são exibidos e o botão "Saiba Mais" é definido
        # Display courses in grid
        cols = st.columns(3)
        for idx, course in active_courses_df.iterrows():
            with cols[idx % 3]:
                # Create card
                with st.container():
                    try:
                        if course['registered'] >= course['slots']:
                            st.image(get_course_image(course['image_path']), use_container_width=True)
                            st.markdown("""
                                <div style='background-color: rgba(255, 0, 0, 0.1); 
                                        padding: 5px; 
                                        border-radius: 5px; 
                                        text-align: center;
                                        color: red;'>
                                    ESGOTADO
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.image(get_course_image(course['image_path']), use_container_width=True)
                    except Exception:
                        st.image(DEFAULT_IMAGE, use_container_width=True)
                    
                    st.subheader(course['name'])
                    st.write(f"Vagas disponíveis: {course['slots'] - course['registered']}")
                    
                    # Modificar o botão "Saiba Mais"
                    if st.button(f"Saiba Mais", key=f"learn_more_{idx}"):
                        st.session_state.current_course = course['name']
                        st.rerun()

        # Registration form
        if st.session_state.current_course:
            # Encontrar o curso selecionado
            selected_course = courses_df[courses_df['name'] == st.session_state.current_course].iloc[0]
            
            st.markdown("---")
            col1, col2 = st.columns([8, 2])
            with col1:
                st.header(f"Inscrição para {selected_course['name']}")
            with col2:
                if st.button("✖ Fechar", type="secondary"):
                    st.session_state.current_course = None
                    st.rerun()
            
            st.markdown(f"""
            **Descrição do Curso:**  
            {selected_course['description']}
            
            **Vagas disponíveis:** {selected_course['slots'] - selected_course['registered']} de {selected_course['slots']}
            """)
            
            if selected_course['registered'] < selected_course['slots']:
                def validate_cpf(cpf):
                    cpf = ''.join(filter(str.isdigit, cpf))
                    if len(cpf) != 11:
                        return False
                    return True
                
                def validate_email(email):
                    import re
                    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                    return re.match(pattern, email) is not None
                
                with st.form("registration_form"):
                    name = st.text_input("Nome Completo")
                    cpf = st.text_input("CPF (apenas números)")
                    email = st.text_input("Email")
                    company = st.text_input("Empresa")
                    
                    if st.form_submit_button("Inscrever-se"):
                        if not name or not cpf or not email or not company:
                            st.error("Por favor, preencha todos os campos.")
                        elif not validate_cpf(cpf):
                            st.error("CPF inválido. Por favor, insira 11 dígitos.")
                        elif not validate_email(email):
                            st.error("Email inválido. Por favor, verifique o formato.")
                        else:
                            save_registration(selected_course['name'], name, cpf, email, company)
                            st.success(f"Inscrição realizada com sucesso para {selected_course['name']}!")
                            st.session_state.current_course = None
                            st.rerun()
            else:
                st.error("Este curso está com vagas esgotadas.")

# Modificar a seção de Course Management para verificar a autenticação da área administrativa
elif page == "Course Management":
    if not st.session_state.authenticated_admin_area:
        st.warning("Por favor, faça login na área de Management no menu lateral.")
    else:
        st.title("Course Management")
        
        # Add tabs for Create and Manage courses
        tab1, tab2 = st.tabs(["Create New Course", "Manage Existing Courses"])
        
        with tab1:
            with st.form("course_form"):
                name = st.text_input("Course Name")
                description = st.text_area("Course Description")
                slots = st.number_input("Available Slots", min_value=1, value=20)
                image_file = st.file_uploader("Course Banner", type=['png', 'jpg', 'jpeg'])
                
                if st.form_submit_button("Save Course"):
                    if name and description and image_file:
                        save_course(name, description, slots, image_file.getvalue())
                        st.success("Course saved successfully!")
                    else:
                        st.error("Please fill all fields")
        
        with tab2:
            courses_df = load_or_create_courses_db()
            if not courses_df.empty:
                for idx, course in courses_df.iterrows():
                    # Garantir que status seja uma string
                    status = str(course['status']).upper() if pd.notna(course['status']) else 'OPEN'
                    with st.expander(f"📚 {course['name']} ({status})"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            new_name = st.text_input("Course Name", course['name'], key=f"name_{idx}")
                            new_description = st.text_area("Description", course['description'], key=f"desc_{idx}")
                            new_slots = st.number_input("Slots", min_value=course['registered'], value=course['slots'], key=f"slots_{idx}")
                            new_image = st.file_uploader("Update Banner", type=['png', 'jpg', 'jpeg'], key=f"img_{idx}")
                            new_status = st.selectbox("Status", ['open', 'completed'], 
                                                    index=0 if course['status'] == 'open' else 1,
                                                    key=f"status_{idx}")
                        
                        with col2:
                            st.image(course['image_path'], use_container_width=True)
                            
                            if st.button("Update", key=f"update_{idx}"):
                                courses_df.loc[idx, 'name'] = new_name
                                courses_df.loc[idx, 'description'] = new_description
                                courses_df.loc[idx, 'slots'] = new_slots
                                courses_df.loc[idx, 'status'] = new_status
                                
                                if new_image:
                                    image_path = os.path.join(IMAGES_DIR, f"{new_name.replace(' ', '_')}.png")
                                    with open(image_path, 'wb') as f:
                                        f.write(new_image.getvalue())
                                    courses_df.loc[idx, 'image_path'] = image_path
                                
                                courses_df.to_excel(COURSES_DB, index=False)
                                st.success("Course updated successfully!")
                                st.rerun()
                            
                            if st.button("Delete", type="secondary", key=f"delete_{idx}"):
                                if course['status'] == 'open' and course['registered'] > 0:
                                    st.error("Cannot delete active course with registered students")
                                else:
                                    # Delete image file
                                    if os.path.exists(course['image_path']):
                                        os.remove(course['image_path'])
                                    # Remove from DataFrame
                                    courses_df = courses_df.drop(idx)
                                    courses_df.to_excel(COURSES_DB, index=False)
                                    st.success("Course deleted successfully!")
                                    st.rerun()
            else:
                st.info("No courses available to manage")

# Modificar a seção de Admin Dashboard para verificar a autenticação da área administrativa
elif page == "Admin Dashboard":
    if not st.session_state.authenticated_admin_area:
        st.warning("Por favor, faça login na área de Management no menu lateral.")
    else:
        st.title("Administrative Dashboard")
        
        courses_df = load_or_create_courses_db()
        registrations_df = load_or_create_registrations_db()
        
        # Display courses statistics
        st.header("Courses Overview")
        
        # Calculate remaining slots
        courses_df['remaining_slots'] = courses_df['slots'] - courses_df['registered']
        
        # Display as a formatted table
        st.dataframe(
            courses_df[['name', 'slots', 'registered', 'remaining_slots', 'status']].style
            .apply(lambda x: ['background-color: #ff4444; color: white; font-weight: bold; border: 1px solid gray; text-align: center' 
                             if x['remaining_slots'] == 0 
                             else 'background-color: #4CAF50; font-weight: bold; border: 1px solid gray; text-align: center' 
                             for i in x], axis=1)
            .format({
                'slots': '{:,.0f}',
                'registered': '{:,.0f}',
                'remaining_slots': '{:,.0f}'
            })
            .set_properties(**{
                'text-align': 'center',
                'font-weight': 'bold',
                'border': '1px solid gray'
            }),
            hide_index=True,
            column_config={
                "name": "Course Name",
                "slots": "Total Slots",
                "registered": "Registered Students",
                "remaining_slots": "Available Slots",
                "status": "Status"
            },
            use_container_width=True
        )