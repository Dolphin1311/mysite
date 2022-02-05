function showDeleteDiv(){
    delete_div = document.getElementsByClassName('delete-div')[0];
    delete_div.style.display = 'block';

    gray_div = document.getElementsByClassName('gray-screen')[0];
    gray_div.style.display = 'block'
}

function hideDeleteDiv(){
    delete_div = document.getElementsByClassName('delete-div')[0];
    delete_div.style.display = 'none';

    gray_div = document.getElementsByClassName('gray-screen')[0];
    gray_div.style.display = 'none'
}