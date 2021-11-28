fetchCarriableData = async () => {
  const res = await fetch("http://0.0.0.0:8000/api/show/", {
    method: "GET",
  });

  //responseオブジェクトからJSONオブジェクトを抽出
  const json = await res.json();

  //取得できたJSONオブジェクトをJSON文字列化して表示
  const string_res = JSON.stringify(json);
  console.log(json['bus']);
  const bus = json['bus'];
  
  let table = document.getElementById('table');

  // 募集しているものがない場合はなしと表示する
  if (bus.length == 0) {
    table.remove();
    let notFound = document.createElement('h2');
    let content = document.createTextNode('現在募集している便はありません');
    notFound.appendChild(content);
    let msgDiv = document.getElementById("msg");
    document.body.insertBefore(notFound, msgDiv);
    return;
  }

  for (let i = 0; i < bus.length; i++) {
    let newRow = table.insertRow();
    const stationData = bus[i];
    console.log(stationData);

    // 企業名を表示
    let newCell = newRow.insertCell();
    let newButton = document.createElement('button');
    newButton.className = 'link-btn';
    newButton.onclick = function () {location.href = '/public/reserve.html';};
    newCell.appendChild(newButton);

    // 企業名を表示
    newCell = newRow.insertCell();
    let newText = document.createTextNode(stationData['name']);
    newCell.appendChild(newText);

    // 駅情報表示
    // 募集開始駅を表示
    newCell = newRow.insertCell();
    newText = document.createTextNode(stationData['station'][0]['name']);
    newCell.appendChild(newText);
    // 開始駅に来る時間
    newCell = newRow.insertCell();
    newText = document.createTextNode(stationData['station'][0]['time']);
    newCell.appendChild(newText);

    // 募集終了駅を表示
    // 駅数
    const stationCount = stationData['station'].length;
    newCell = newRow.insertCell();
    newText = document.createTextNode(stationData['station'][stationCount-1]['name']);
    newCell.appendChild(newText);
    // 最終駅に到着する時間
    newCell = newRow.insertCell();
    newText = document.createTextNode(stationData['station'][stationCount-1]['time']);
    newCell.appendChild(newText);

    // 最大量の表示
    newCell = newRow.insertCell();
    newText = document.createTextNode(stationData['max_size']);
    newCell.appendChild(newText);
  }
};

function myRedirect(carrybusId) {
  location.href = '/public/reserve.html';
  console.log(carrybusId);
}