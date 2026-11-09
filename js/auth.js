
import { supabase } from './supabase.js';

// Cadastrar um aluno
export async function cadastrarUsuario(nome, email, senha) {
    const { data, error } = await supabase.auth.signUp({
        email: email,
        password: senha,
        options: {
            data: {
                nome: nome
            }
        }
    });

    if (error) {
        throw error;
    }

    return data;
}

// Fazer login
export async function entrarUsuario(email, senha) {
    const { data, error } = await supabase.auth.signInWithPassword({
        email: email,
        password: senha
    });

    if (error) {
        throw error;
    }

    // Buscar o tipo de usuário cadastrado
    const { data: perfil, error: erroPerfil } = await supabase
        .from('profiles')
        .select('nome, tipo_usuario')
        .eq('id', data.user.id)
        .single();

    if (erroPerfil) {
        throw erroPerfil;
    }

    return {
        usuario: data.user,
        perfil: perfil
    };
}
