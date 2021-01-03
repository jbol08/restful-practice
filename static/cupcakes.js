
function generateCupcake(cupcake) {
    return `<div data-cupcake-id=${cupcake.id}>
        <li> ${cupcake.flavor} ${cupcake.size} ${cupcake.rating}
        <button class="delete-button">X </button> </li>
        <img src="${cupcake.img}"> </div>`;
}

async function showCupcakes() {
    const response = await axios.get('http://localhost:5000/api/cupcakes');
  
    for (let cupcakeData of response.data.cupcakes) {
      let newCupcake = $(generateCupcake(cupcakeData));
      $("#cupcakes-list").append(newCupcake);
    }
  }
  


$('#new-cupcake').on('submit', async function (event) {
    event.preventDefault();

    let flavor = $('#form-flavor').val();
    let size = $('#form-size').val();
    let rating = $('#form-rating').val();
    let image = $('#form-image').val();

    const newCupcake = await axios.post('http://localhost:5000/api/cupcakes', { flavor, size, rating, image });

    let newCupcake = $(generateCupcake(newCupcake.data.cupcake));
    $('#cupcake-list').append(newCupcake)
    $('#new-cupcake').trigger('reset');
});



$('#cupcake-list').on('click', ".delete-button", async function (event) {
    event.preventDefault();

    let $cupcake = $(event.target).closest("div");
    let cupcakeId = $cupcake.attr('data-cupcake-id');

    await axios.delete(`http://localhost:5000/api/${cupcakeId}`);
    $cupcake.remove();
});

$(showCupcakes);



