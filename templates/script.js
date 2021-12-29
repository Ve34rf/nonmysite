but.addEventListener("click", testo)

async function testo() {
    let response = await fetch('http://127.0.0.1:8000/testo/', {
        method:"POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({"data":data.value})
    })
    console.log(await data.value);
    let res = await response.json();
    console.log(await res);
}