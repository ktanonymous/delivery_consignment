function feeCheck() {
  const baggageId = feeForm.baggage_id.value;

  if (baggageId) {

    dataSet = {
      "baggage_id": baggageId,
    }

    postfee(dataSet);
  }
}

getFee = async () => {
  const res = await fetch("http://0.0.0.0:8000/api/fee/", {
    method: "GET",
  });

  //responseオブジェクトからJSONオブジェクトを抽出
  const json = await res.json();

  let feeDisplay = document.createElement('h2');
  let content = document.createTextNode(json['fee'] + '円');
  feeDisplay.appendChild(content);

  let feeDiv = document.getElementById("fee");
  document.body.insertBefore(feeDisplay, feeDiv);

  //取得できたJSONオブジェクトをJSON文字列化して表示
  const string_res = JSON.stringify(json);
  console.log(string_res);
};

getFee();