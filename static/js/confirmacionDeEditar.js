const datos_correctos= document.querySelectorAll('.btn-block'); //guardamos todo en variable block scope
if(datos_correcto) { //si existe
  const btnArray = Array.from(datos_correcto); //le pasamos el valor a una variable
  btnArray.forEach((btn) => { //llama a una función una vez para cada elemento
    btn.addEventListener('click', (e) => { //le asignamos un ebento el cual nos dara falso o verdadero
      if(!confirm('¿Esta seguro de editar este dato?')){ //si preciona cancelar
      	alert("El dato no se edito" );
        e.preventDefault();  //solo salte y no agas nada  de lo contrario se eliminara el dato
      }
    });
  })
}
