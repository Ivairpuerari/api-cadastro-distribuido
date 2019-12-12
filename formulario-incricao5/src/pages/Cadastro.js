import React , {Component} from 'react';

import './Cadastro.css';
import api from '../services/api';


class Cadastro extends Component {

    state = {
        nome: '',
        email: '',
        matricula: ''
    };

    handleSubmit = async e => {
        
            const data = new FormData();
            data.append('nome', this.state.nome);
            data.append('email', this.state.email);
            data.append('matricula', this.state.matricula);

            console.log(data.values);
            await api.post(`/inscricao?nome=${this.state.nome}&email=${this.state.email}&matricula=${this.state.matricula}`);
            this.props.history.push('/');
            
    }


    handleImageChange = e => {
        this.setState({ image: e.target.files[0] });
    }

    handleChange = e => {
        this.setState({ [e.target.name]: e.target.value});

    }

    render() {
     return (
         
        <form id = "new-post" onSubmit={(e) =>this.handleSubmit(e)}>
          <h2>Faça seu Check-in</h2>
           <input  
                type="text"
                name="nome"
                placeholder="nome"
                onChange ={this.handleChange}
                value={this.state.nome}
            />

            <input  
                type="text"
                name="email"
                placeholder="E-mail"
                onChange={this.handleChange}
                value={this.state.email}
            />
            
           <input  
                type="text"
                name="matricula"
                placeholder="Matricula"
                onChange={this.handleChange}
                value={this.state.matricula}
            />

        <button type="submit">Enviar</button>
         
        </form>
     );
    }
}

export default Cadastro;
