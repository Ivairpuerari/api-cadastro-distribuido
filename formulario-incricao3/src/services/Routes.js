import React from 'react'
import {Switch, Route} from 'react-router-dom'

import Cadastro from '../pages/Cadastro';
import Lista from '../pages/lista';

function Routes(){
    return (
        <Switch>
            <Route exact path="/"  component={Cadastro} />
            <Route exact path="/listar"  component={Lista} />
        </Switch>
    );
}

export default Routes;


