const open_ingredient_window = (passed_data) => {
    passed_url = "/ingredients/show_one/semi_view/" + passed_data;
    window.open(
        passed_url,
        "",
        "height=500,width=600,menubar=no,resizable=yes"
    );
};

const spell_lookup = async (table, search_string) => {
    let tableBody = table.querySelector("tbody");
    let res = await fetch(
        `https://api.spoonacular.com/food/ingredients/search?apiKey=e5435bd9712a45208d0da9ad28db16b2&query=${search_string}`
    );
    let data = await res.json();
    let { results } = data;
    tableBody.innerHTML = "";
    for (const row of results) {
        const rowElement = document.createElement("tr");
        const nameCellElement = document.createElement("td");
        nameCellElement.textContent = row.name;
        rowElement.appendChild(nameCellElement);

        const imageCellElement = document.createElement("td");
        const imageCellImage = document.createElement("img");
        imageCellImage.src =
            "https://spoonacular.com/cdn/ingredients_100x100/" + row.image;
        imageCellImage.style = "width: 100px; height: auto;";
        imageCellElement.appendChild(imageCellImage);
        rowElement.appendChild(imageCellElement);

        const actionsCellElement = document.createElement("td");
        const actionsAddToSpellbook = document.createElement("a");
        actionsAddToSpellbook.textContent = "Add to Spellbook";
        actionsAddToSpellbook.href = "/ingredients/show_one/" + row.id;

        actionsCellElement.appendChild(actionsAddToSpellbook);
        rowElement.appendChild(actionsCellElement);
        tableBody.appendChild(rowElement);
    }
};

const recipe_lookup = async (table, search_string) => {
    let tableBody = table.querySelector("tbody");
    let res = await fetch(
        `https://api.spoonacular.com/recipes/complexSearch?apiKey=e5435bd9712a45208d0da9ad28db16b2&query=${search_string}`
    );
    let data = await res.json();
    let { results } = data;
    tableBody.innerHTML = "";
    for (const row of results) {
        const rowElement = document.createElement("tr");
        let idCellElement = document.createElement("td");
        idCellElement.textContent = row.id;
        rowElement.appendChild(idCellElement);

        const nameCellElement = document.createElement("td");
        nameCellElement.textContent = row.title;
        rowElement.appendChild(nameCellElement);

        const imageCellElement = document.createElement("td");
        const imageCellImage = document.createElement("img");
        imageCellImage.src = row.image;
        imageCellElement.appendChild(imageCellImage);
        rowElement.appendChild(imageCellElement);

        const actionsCellElement = document.createElement("td");
        const actionsAddToBosses = document.createElement("a");
        actionsAddToBosses.textContent = "Convert to Boss";
        actionsAddToBosses.href = "/recipes/show_one/" + row.id;
        const actionsPipeElement = document.createElement("span");
        actionsPipeElement.textContent = " | ";
        const actionsAddToFavorites = document.createElement("a");
        actionsAddToFavorites.textContent = "Add to Favorites";
        actionsAddToFavorites.href = "/recipes/add_favorite/" + row.id;

        actionsCellElement.appendChild(actionsAddToBosses);
        actionsCellElement.appendChild(actionsPipeElement);
        actionsCellElement.appendChild(actionsAddToFavorites);
        rowElement.appendChild(actionsCellElement);
        tableBody.appendChild(rowElement);
    }
};

const expiration_bars = (statusdiv, expiration_date) => {
    let date = new Date();
    let day = date.getDate();
    let month = date.getMonth() + 1;
    if (month < 10) {
        month = "0" + month;
    }
    expiration_date = expiration_date.replaceAll("-", "");
    let year = date.getFullYear();
    let current_date = `${year}${month}${day}`;

    let days_to_expire = expiration_date - current_date;
    console.log(days_to_expire);

    style_box = "height: 10px;";
    if (days_to_expire > 5) {
        style_box = style_box + "background-color : green;";
    } else if (days_to_expire <= 5 && days_to_expire > 3) {
        style_box = style_box + "background-color : yellow;";
    } else if (days_to_expire <= 3) {
        style_box = style_box + "background-color : red;";
    }
    style_width = days_to_expire * 10;
    if (style_width > 400) {
        style_width = 400;
    }
    style_box = style_box + `width: ${style_width}px;`;
    console.log(style_box);
    statusdiv.style = style_box;
};

const calculate_charges = (amount, charge_amount, table_element) => {
    console.log(amount.innerText);
    console.log(charge_amount.value);
    console.log(table_element.innerText);
    table_element.innerText = amount.innerText / charge_amount.value;
};
