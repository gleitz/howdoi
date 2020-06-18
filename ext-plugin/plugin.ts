"use strict";
import * as cp from "child_process";

const HOWDOI_PREFIX = 'howdoi';

interface HowdoiResult {
    question: string;
    answer: string[];
    link: string[];   
}

function main(arg:string) {
    const userCommand:string = arg;
    const userCommandWithoutComment:string[]|null = modifyCommentedText(userCommand);
    
    if (userCommandWithoutComment != null) {
        const textToBeSearched:string = userCommandWithoutComment[0];
        const commentBegin:string  = userCommandWithoutComment[1];
        const commentEnd:string = userCommandWithoutComment[2];

        spawnChild(textToBeSearched, function(howdoiOutput:string) {
            howdoiResult(howdoiOutput, userCommand, commentBegin, commentEnd);
        });
    }   
}

async function spawnChild(command:string, callback:any) {
    const commandWithoutPrefix = removeHowdoiPrefix(command);
    const process = await cp.spawn("howdoi", [commandWithoutPrefix, '-n 3']);
    let howdoiCommandOutput:string = '';
    process.stdout.on("data", (data:any) => {
        howdoiCommandOutput += String(data);
    });

    process.stderr.on("data", (data:any) => {
        console.log(`stderr: ${data}`);
    });
    
    process.on('error', (error:any) => {
        console.log(`error: ${error.message}`);
    });
    
    process.on("close", (code:any) => {
        console.log(`child process exited with code ${code}`);
        callback(howdoiCommandOutput);
    });
}

function removeHowdoiPrefix(command:string) {
    if (!command.trim().startsWith(HOWDOI_PREFIX)) {
        return command;
    }
    return command.replace(HOWDOI_PREFIX, '');
}

function modifyCommentedText(textToBeModified:string): string[]|null {
    /* This function finds the comment regex, removes it from the string and returns an array 
    with the modified string, the beginning comment regex, ending comment regex */
    const commentStartRegex:RegExp =  /^[!@#<>/\$%\^\&*\)\(+=._-]+/;
    const commentEndRegex:RegExp = /[!@#<>/\$%\^\&*\)\(+=._-]+$/;
    let commentBegin:string;
    let commentEnd:string;	
    let result:string[];
        
    if (textToBeModified.match(commentStartRegex) && textToBeModified.match(commentEndRegex)){
        commentBegin = textToBeModified.match(commentStartRegex)!.join();
        commentEnd = textToBeModified.match(commentEndRegex)!.join();
        textToBeModified = textToBeModified.replace(commentStartRegex, '');
        textToBeModified = textToBeModified.replace(commentEndRegex, '');
        result = [textToBeModified, commentBegin, commentEnd];
        return result;
    }
    else if(textToBeModified.match(commentEndRegex)){
        commentEnd = textToBeModified.match(commentEndRegex)!.join();
        textToBeModified = textToBeModified.replace(commentEndRegex, '');
        result = [textToBeModified,'',commentEnd];
        return result;
    }
    else if(textToBeModified.match(commentStartRegex)){
        commentBegin = textToBeModified.match(commentStartRegex)!.join();
        textToBeModified = textToBeModified.replace(commentStartRegex, '');
        result= [textToBeModified, commentBegin, ''];
        return result;
    }
    else {
        return null;
    }
}

function organizeHowdoiOutput(howdoiOutput:string, commentBegin:string, commentEnd:string): string[][] {
    /* Creates an array from the howdoiOutput string in which each element 
    is one of three answers from the usersCommand */
    let howdoiAnswersArr = howdoiOutput.split('\n'+'================================================================================' + '\n' + '\n');
    /* Creates a 2D array from howdoiAnswersArr in which each element is an array which denotes
     one of three answers from the usersCommand, and the elements in that array are link and answer */
    let newHowdoiAnswersArr:string[][] = howdoiAnswersArr.map((elem) => elem.split(' ★'));
    //  The comment Regex is added to the link string
    for (let i = 0; i < newHowdoiAnswersArr.length; i++) {
        newHowdoiAnswersArr[i][0] = commentBegin + newHowdoiAnswersArr[i][0] + commentEnd;
    }

    return newHowdoiAnswersArr;
}

function createHowdoiResult(howdoiResultArr:string[][], userCommand:string): HowdoiResult {
    let howdoiResultObj:HowdoiResult = {question: userCommand, answer: [], link: []};
    
    for (let i = 0; i < howdoiResultArr.length; i++) {
        howdoiResultObj.link.push(howdoiResultArr[i][0]);
        howdoiResultObj.answer.push(howdoiResultArr[i][1]);
    }

    return howdoiResultObj;
}

function howdoiResult(howdoiOutput:string, userCommand:string, commentBegin:string, commentEnd:string): HowdoiResult {
    const organizedHowdoiArr:string[][] = organizeHowdoiOutput(howdoiOutput, commentBegin, commentEnd);
    const howdoiResultObj:HowdoiResult = createHowdoiResult(organizedHowdoiArr, userCommand);
    return howdoiResultObj;
}