import React , {Component} from 'react';

import './Cadastro.css';
import api from '../services/api';


class Lista extends Component
{
   
        
    state = {
            linhas : ' '
    };
   

    componentDidMount()
    {

       const data = api.get("todos-inscritos").then(response => {
            return response.body
        }).catch(error => {
            console.log(error)
        })
          
         this.setState({
             linhas : data.text
         });
    var string = this.linhas.split(",");

      
        console.log(string); 
        this.setState( { rows: string, columns: "teste"} );
        


    }

    render()
    {

        return (
            <div id="container" className="container">
                <h2>Lista de inscritos</h2>
                <table className="table">
                    
                </table>
            </div>
        )
    }
}

export default Lista;