// 二次元配列の先頭の要素からindexを探す
function searchIndex(array, key) {
  let index = array.filter(data => data.name == key);
  return index;
}



function reserveCheck() {
  const startStation = reserveForm.start_station.value;
  const endStation = reserveForm.end_station.value;
  const size = reserveForm.size.value;

  if (startStation && endStation && size) {
    // localstrage に入っているデータをjson形式にして取得
    carriableBus = JSON.parse(window.localStorage.getItem('carriable_bus'));
    // 駅の情報から荷物を乗せる駅とおろす駅のインデックスを取得
    stationData = carriableBus['station'];
    startData = searchIndex(stationData, startStation)[0];
    endData = searchIndex(stationData, endStation)[0];

    dataSet = {
      "bus_id": carriableBus['carry_bus_id'],
      "start_station": startData['name'],
      "end_station": endData['name'],
      "start_time": startData['time'],
      "end_time": endData['time'],
      "size": size,
      "station_data": stationData
    }

    postReserve(dataSet);
  }
}

postReserve = async (dataSet) => {
  console.log(dataSet);
  console.log(typeof dataSet);
  const res = await fetch("http://0.0.0.0:8000/api/reserve/", {
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

console.log(JSON.parse(window.localStorage.getItem('carriable_bus')));