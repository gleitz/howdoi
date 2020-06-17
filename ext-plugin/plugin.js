"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
exports.__esModule = true;
var cp = require("child_process");
main();
function main() {
    var txt = '# howdoi print python';
    var txtArr = modifyCommentedText(txt);
    var textToBeSearched = txtArr[0];
    var commentBegin = txtArr[1];
    var commentEnd = txtArr[2];
    spawnChild(textToBeSearched, function (myArr) {
        helperFunc(myArr, txt, commentBegin, commentEnd);
    });
}
//  process
function spawnChild(command, callback) {
    return __awaiter(this, void 0, void 0, function () {
        var updatedCommand, process, result;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    updatedCommand = howdoiPrefix(command);
                    return [4 /*yield*/, cp.spawn("howdoi", [updatedCommand, '-n 3'])];
                case 1:
                    process = _a.sent();
                    result = [];
                    process.stdout.on("data", function (data) {
                        result.push(String(data));
                    });
                    process.stderr.on("data", function (data) {
                        console.log("stderr: " + data);
                    });
                    process.on('error', function (error) {
                        console.log("error: " + error.message);
                    });
                    process.on("close", function (code) {
                        console.log("child process exited with code " + code);
                        callback(result);
                    });
                    return [2 /*return*/];
            }
        });
    });
}
// removes howdoi from command
function howdoiPrefix(command) {
    var prefix = "howdoi";
    if (command.includes(prefix)) {
        var newCommand = command.replace(prefix, '');
        return newCommand;
    }
    else {
        return command;
    }
}
//  only for single line comments
function modifyCommentedText(textToBeModified) {
    var regexBegins = /^[!@#<>/\$%\^\&*\)\(+=._-]+/;
    var regexEnds = /[!@#<>/\$%\^\&*\)\(+=._-]+$/;
    var commentBegin;
    var commentEnd;
    if (textToBeModified.match(regexBegins) && textToBeModified.match(regexEnds)) {
        commentBegin = textToBeModified.match(regexBegins).join();
        commentEnd = textToBeModified.match(regexEnds).join();
        textToBeModified = textToBeModified.replace(regexBegins, '');
        textToBeModified = textToBeModified.replace(regexEnds, '');
        var result = [textToBeModified, commentBegin, commentEnd];
        return result;
    }
    else if (textToBeModified.match(regexEnds)) {
        commentEnd = textToBeModified.match(regexEnds).join();
        textToBeModified = textToBeModified.replace(regexEnds, '');
        var result = [textToBeModified, '', commentEnd];
        return result;
    }
    else if (textToBeModified.match(regexBegins)) {
        commentBegin = textToBeModified.match(regexBegins).join();
        textToBeModified = textToBeModified.replace(regexBegins, '');
        var result = [textToBeModified, commentBegin, ''];
        return result;
    }
    else {
        var result = [textToBeModified, '', ''];
        return result;
    }
}
function spliceArr(obj, commentBegin, commentEnd) {
    var dataString = String(obj);
    var lines = dataString.split('\n' + '================================================================================' + '\n' + '\n');
    var newArr = lines.map(function (elem) { return elem.split(' ★'); });
    for (var i = 0; i < newArr.length; i++) {
        newArr[i][0] = commentBegin + newArr[i][0] + commentEnd;
    }
    return newArr;
}
function helperFunc(resultArr, userTxt, commentBegin, commentEnd) {
    console.log('in helperfunc');
    var newResult = spliceArr(resultArr, commentBegin, commentEnd);
    console.log('result', newResult[0][0]);
}
