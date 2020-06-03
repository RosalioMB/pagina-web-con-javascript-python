const confirmacion_de_borrar = document.querySelectorAll('.btn-delete'); //guardamos todo en variable block scope
if(confirmacion_de_borrar) { //si existe
  const btnArray = Array.from(confirmacion_de_borrar); //le pasamos el valor a una variable
  btnArray.forEach((btn) => {  //llama a una función una vez para cada elemento
    btn.addEventListener('click', (e) => { //le asignamos un ebento el cual nos dara falso o verdadero
      if(!confirm('¿Esta seguro de eliminar el dato?')){ //si preciona cancelar
      	alert("El dato no se elimino" );
        e.preventDefault(); //solo salte y no agas nada  de lo contrario se eliminara el dato
      } 
    });
  })
}
