
const institutes = require('./institute.json');
const fs = require('fs');
const path = require('path')
const XLSX = require('XLSX')
const preparedInstitutes = require('./preparedInstitutes.json');
const preparedPrivateUni = require('./preparedPrivateUni.json');
const publicUni = require('./publicUni.json');

function prepareInstitutes () {
    let result = institutes.filter(i => i != "").map(i => {
        var n = i.indexOf(' – ')
        if (n == -1) return i
        return i.substring(0, n);
    })
    saveData(result, 'preparedInstitutes')
}

function preparePrivateUni () {
    const workbook = XLSX.readFile('./privateUni.xls')
    var sheetName = workbook.SheetNames[0];
    var sheet = workbook.Sheets[sheetName]
    sheet['!ref'] = 'B4:G386'

    var xlData = XLSX.utils.sheet_to_json(sheet, { header: 1 });

    let result = xlData.map(d => d[1])
    saveData(result, 'preparedPrivateUni')
}

function saveData (data, filename) {
    const serialized = JSON.stringify(data, null, 2)
    fs.writeFileSync(path.join(__dirname, '', filename + '.json'), serialized, 'utf-8')
}

function savetxt (data, filename) {
    fs.writeFileSync(path.join(__dirname + '/out', '', filename + '.txt'), data, 'utf-8')
}

function prepareGooglePatentsQuery (data, filename) {
    for (i = 0, l = data.length; i * 25 < l; i ++) {
        chunk = data.slice(i, i + 25);
        const result = chunk.reduce((x, y) => x + ` assignee:(${y})`, "")
        savetxt(result, filename + i)
    }
}

prepareGooglePatentsQuery(preparedInstitutes, 'institutesQuery')
prepareGooglePatentsQuery(preparedPrivateUni, 'privateUniQuery')
prepareGooglePatentsQuery(publicUni, 'publicUniQuery')