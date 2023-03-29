const input_type_select = document.getElementById('input_type');
const steam_id_input_div = document.getElementById('steam_id_input');
const game_list_input_div = document.getElementById('game_list_input');

input_type_select.addEventListener('change', function () {
    if (input_type_select.value === 'steam_id') {
        steam_id_input_div.style.display = 'block';
        game_list_input_div.style.display = 'none';
    } else if (input_type_select.value === 'none') {
        steam_id_input_div.style.display = 'none';
        game_list_input_div.style.display = 'none';
    } else {
        steam_id_input_div.style.display = 'none';
        game_list_input_div.style.display = 'block';
    }
});