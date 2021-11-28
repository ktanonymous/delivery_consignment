function formatDate (date) {
  let formatted_date = date.getDate() + "-" + months[date.getMonth()] + "-" + date.getFullYear()
  return formatted_date;
}

function recruitCheck() {
  const name = recruitForm.name.value;
  const startStation = recruitForm.start_station.value;
  const endStation = recruitForm.end_station.value;
  const startTime = recruitForm.start_time.value;
  const endTime = recruitForm.end_time.value;
  const maxSize = recruitForm.max_size.value;

  if (name && startStation && endStation && startTime && endTime && maxSize) {
    const start = new Date(startTime);
    console.log(startTime);
    console.log(start);
    dataSet = {
      "name": name,
      "start_station": startStation,
      "end_station": endStation,
      "start_time": start,
      "end_time": endTime,
      "max_size": maxSize,
    }

    postRecruit(dataSet);
  }
}

postRecruit = async (dataSet) => {
  console.log(dataSet);
  console.log(typeof dataSet);
  const res = await fetch("http://0.0.0.0:8000/api/recruit/", {
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
