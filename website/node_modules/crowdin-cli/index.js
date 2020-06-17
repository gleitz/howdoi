/*jslint node:true*/
'use strict';

var api = require('./api'),
    YAML = require('yamljs'),
    fs = require('fs'),
    configFileName = 'crowdin.yaml';

if (!fs.existsSync(configFileName)) {
    console.log("Configuration file is missing.");
    process.exit(1);
}

var content = fs.readFileSync(configFileName, 'utf8'),
    config = YAML.parse(content),
    base_path = config.base_path || '.';

if (config.api_key === undefined) {
    console.log("API key is missing.");
    process.exit(1);
}

if (config.base_url !== undefined) {
    api.setKey(config.base_url);
}

api.setKey(config.api_key);
var handleTestResult = function (err, data) {
    if (err) {
        throw err;
    }

    console.log(data);
};
//api.projectInfo(config.project_identifier, handleTestResult);
//api.supportedLanguages(handleTestResult);
//api.downloadTranslations(config.project_identifier, 'es').pipe(fs.createWriteStream('es.zip'));
//api.downloadAllTranslations(config.project_identifier).pipe(fs.createWriteStream('all.zip'));
//api.downloadTranslationMemory(config.project_identifier).pipe(fs.createWriteStream('cordova.tmx'));
//api.uploadGlossary(config.project_identifier, 'cordova.tbx');
//api.uploadGlossary(config.project_identifier, fs.createReadStream('cordova.tbx'));
//api.uploadTranslationMemory(config.project_identifier, 'cordova.tmx');
//api.createDirectory(config.project_identifier, 'test', handleTestResult);
//api.deleteDirectory(config.project_identifier, 'test', handleTestResult);
//api.changeDirectory(config.project_identifier, 'test', { new_name: 'test1', title: 'Test directory', export_pattern: '%original_path%/%two_letters_code%' }, handleTestResult);
//api.changeDirectory(config.project_identifier, 'test1', { new_name: 'test', title: '', export_pattern: 'test' }, handleTestResult);
//api.editProject(config.project_identifier, { name: 'Cordova test 1' }, handleTestResult);
//api.addFile(config.project_identifier, ['test/1.md', 'test/adas.md'], {}, handleTestResult);

module.exports = api;
