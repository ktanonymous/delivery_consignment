function formatDate (date) {
  let formatted_date = date.getDate() + "-" + months[date.getMonth()] + "-" + date.getFullYear()
  return formatted_date;
}

function setCheck() {
  const name = setForm.name.value;
  const time = setForm.time.value;
  const busId = setForm.bus_id.value;

  if (name && time && busId) {
    dataSet = {
      "name": name,
      "time": time,
      "bus_id": busId
    }

    postSet(dataSet);
  }
}

postSet = async (dataSet) => {
  console.log(dataSet);
  console.log(typeof dataSet);
  const res = await fetch("http://0.0.0.0:8000/api/time_table/", {
    method: "POST",
    body: JSON.stringify(dataSet),
    headers: {
      'Content-Type': 'application/json',
      'Accept': '*/*',
    },
  });

  //responseオブジェクトからJSONオブジェクトを抽出
  const json = await res.json();

  //取得できたJSONオブジェクトをJSON文字列化して表示
  const string_res = JSON.stringify(json);
  console.log(string_res);
};
