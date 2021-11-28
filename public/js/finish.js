function finishCheck() {
  const baggageId = finishForm.baggage_id.value;

  if (baggageId) {

    dataSet = {
      "baggage_id": baggageId,
    }

    postFinish(dataSet);
  }
}

postFinish = async (dataSet) => {
  console.log(dataSet);
  console.log(typeof dataSet);
  const res = await fetch("http://0.0.0.0:8000/api/finish/", {
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