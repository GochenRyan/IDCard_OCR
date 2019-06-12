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

// 生成uuid,用于区别
function uuid() {
    var s = [];
    var hexDigits = "0123456789abcdef";
    for (var i = 0; i < 36; i++) {
        s[i] = hexDigits.substr(Math.floor(Math.random() * 0x10), 1);
    }
    s[14] = "4";  // bits 12-15 of the time_hi_and_version field to 0010
    s[19] = hexDigits.substr((s[19] & 0x3) | 0x8, 1);  // bits 6-7 of the clock_seq_hi_and_reserved to 01
    s[8] = s[13] = s[18] = s[23] = "-";

    var uuid = s.join("");
    return uuid;
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

var UUID = uuid();

$(function () {
    $("#imgUpload").click(function () {
        var fileObj = document.getElementById("imgSelect").files[0];    //js获取文件对象
        if(typeof (fileObj) == "undefines" || fileObj.size <= 0){
            alert("请选择图片");
        }
        var formFile = new FormData();
        formFile.append("file", fileObj);
        formFile.append("uuid", UUID);
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

var z = 0;

function show(pic){
    if(z < pic.length) {
        $("#analysisImg").attr("src", pic[z]);
        setTimeout(()=>show(pic),1000);
    }
    z++;
}

$(function () {
    $("#analysisBtn").click(function () {
        $.ajax({
            url:"/analysis/",
            type: "POST",
            data: UUID,
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {
                //显示解析图片
                var path = "static\\analysisImgs\\".concat(UUID);
                var pic = [path.concat("\\gray.jpg"),path.concat("\\binary.jpg"),path.concat("\\dilation.jpg"),path.concat("\\erosion.jpg")];
                z = 0;
                show(pic);

                obj = JSON.parse(data);
                $("#cardName").val(obj.name);
                $("#cardSex").val(obj.sex);
                $("#cardEthnicity").val(obj.ethnicity);
                $("#cardYear").val(obj.year);
                $("#cardMonth").val(obj.month);
                $("#cardDay").val(obj.day);
                $("#cardAddress").val(obj.address);
                $("#cardIDNumber").val(obj.id_number);
                $("#cardFace").attr("src",obj.face);
                $("#modifyBtn").removeAttr("disabled");
                $("#cardIDNumber").attr("readonly",true);

                UUID = uuid();
            },
            error: function () {
                alert("解析失败！");
            }
        });
    });
});




$(function () {
    $("#modifyBtn").click(function () {
        var info = JSON.stringify({"name":$("#cardName").val(),"sex":$("#cardSex").val(),"ethnicity":$("#cardEthnicity").val(),"year":$("#cardYear").val(),
            "month":$("#cardMonth").val(),"day":$("#cardDay").val(), "address":$("#cardAddress").val(),"id_number":$("#cardIDNumber").val()});
        $.ajax({
            url:"/modify/",
            type: "POST",
            data: info,
            cache: false,
            contentType: 'application/json;charset=utf-8',
            processData: false,
            success: function () {
                alert("修改成功！");
            },
            error: function () {
                alert("修改失败！");
            }
        });
    });
});