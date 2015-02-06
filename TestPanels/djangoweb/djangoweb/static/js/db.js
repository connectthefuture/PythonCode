function getdb(){
    var db = openDatabase('html5app', '1.0', 'html5app DB', 10 * 1024 * 1024);
    return db;
}

function test(){
    db.executeSql("select * from mysite_Vocabulary")

}