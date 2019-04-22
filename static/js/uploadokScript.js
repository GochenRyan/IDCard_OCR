// var info = document.getElementById('idCard').getAttribute('d');
// obj = JSON.parse(info);
// document.getElementById('cardName').innerHTML = obj.name;
// document.getElementById('cardSex').innerHTML = obj.sex;
// document.getElementById('cardEthnicity').innerHTML = obj.ethnicity;
// document.getElementById('cardYear').innerHTML = obj.year;
// document.getElementById('cardMonth').innerHTML = obj.month;
// document.getElementById('cardDay').innerHTML = obj.day;
// document.getElementById('cardAddress').innerHTML = obj.address;
// document.getElementById('cardIDNumber').innerHTML = obj.id_number;

if (typeof FileReader == 'undefined') {
    alert("当前浏览器不支持FileReader接口");
    //使选择控件不可操作
    document.getElementById("imgSelect").setAttribute("disabled", "disabled");
}

//选择图片，马上预览
function selectImg(obj) {
    var file = obj.files[0];

    console.log(obj);
    console.log(file);
    console.log("file.size = " + file.size);  //file.size 单位为byte

    var reader = new FileReader();

    //读取文件过程方法
    reader.onloadstart = function (e) {
        console.log("开始读取....");
    };
    reader.onprogress = function (e) {
        console.log("正在读取中....");
    };
    reader.onabort = function (e) {
        console.log("中断读取....");
    };
    reader.onerror = function (e) {
        console.log("读取异常....");
    };
    reader.onload = function (e) {
        console.log("成功读取....");
        var img = document.getElementById("previewImg");
        img.src = e.target.result;
        //或者 img.src = this.result;  //e.target == this
    };
    reader.readAsDataURL(file);
}

$(function () {
    $("#imgUpload").click(function () {
        var fileObj = document.getElementById("imgSelect").files[0];    //js获取文件对象
        if(typeof (fileObj) == "undefines" || fileObj.size <= 0){
            alert("请选择图片");
        }
        var formFile = new FormData();
        formFile.append("file", fileObj);
        $.ajax({
            url: "/upload/",
            type: "POST",
            data: formFile,
            // dataType: "json",
            cache:false,
            contentType: false,
            processData: false,
            success: function (data) {
                if(data == "error_type"){
                    alert("请上传图片！");
                }else{
                    $("#analysisBtn").removeAttr("disabled")
                }
            },
            error: function () {
              alert("上传失败！");
            }
        });
    });
});