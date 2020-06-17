/*jslint node: true, nomen: true*/
'use strict';

var https = require('https'),
    fs = require('fs'),
    querystring = require('querystring'),
    request = require('request'),
    extend = require('util')._extend,
    apiKey,
    baseUrl = 'https://api.crowdin.com',
    verbose = 0;

function validateKey() {
    if (apiKey === undefined) {
        throw new Error("Please specify CrowdIn API key.");
    }
}

function getApiCall(apiUrl, callback) {
    validateKey();
    var url = baseUrl + '/api/' + apiUrl,
        params = { json: true, key: apiKey };
    if (verbose > 0) {
        console.log("Doing GET request:");
        console.log(url);
    }

    return request.get({ url: url, qs: params }, function (error, response, body) {
        if (callback) {
            if (!error && response.statusCode === 200) {
                callback(null, JSON.parse(body));
            } else {
                callback(error);
            }
        } else {
            if (error) {
                throw error;
            }
        }
    });
}

function postApiCall(apiUrl, getOptions, callback) {
    validateKey();
    if (callback === undefined) {
        callback = getOptions;
        getOptions = {};
    }

    var url = baseUrl + '/api/' + apiUrl,
        params = extend(getOptions, { json: true, key: apiKey });
    if (verbose > 0) {
        console.log("Doing POST request:");
        console.log(url);
    }

    return request.post({ url: url, qs: params }, function (error, response, body) {
        if (callback) {
            if (!error && response.statusCode === 200) {
                callback(null, JSON.parse(body));
            } else {
                callback(error);
            }
        } else {
            if (error) {
                throw error;
            }
        }
    });
}

function postApiCallWithFormData(apiUrl, getOptions, postOptions, callback) {
    validateKey();
    if (callback === undefined) {
        callback = postOptions;
        postOptions = getOptions;
        getOptions = {};
    }

    var url = baseUrl + '/api/' + apiUrl,
        params = extend(getOptions, { json: true, key: apiKey });
    if (verbose > 0) {
        console.log("Doing POST request:");
        console.log(url);
    }

    return request.post({ url: url, qs: params, formData: postOptions || {} }, function (error, response, body) {
        if (callback) {
            if (!error && response.statusCode === 200) {
                callback(null, JSON.parse(body));
            } else {
                callback(error);
            }
        } else {
            if (error) {
                throw error;
            }
        }
    });
}

function getApiRequest(apiUrl, callback) {
    validateKey();
    var url = baseUrl + '/api/' + apiUrl + '?key=' + apiKey + '&json';
    if (verbose > 0) {
        console.log("Doing request:");
        console.log(url);
    }

    return request(url);
}

module.exports = {
    setVerbose: function (newValue) {
        verbose = newValue;
    },
    setBasePath: function (newBasePath) {
        baseUrl = newBasePath;
    },
    setKey: function (newKey) {
        apiKey = newKey;
    },
    /**
    * Add new file to Crowdin project
    * @param projectName {String} Should contain the project identifier
    * @param files {Array} Files array that should be added to Crowdin project.
    *   Array keys should contain file names with path in Crowdin project.
    *   Note! 20 files max are allowed to upload per one time file transfer.
    * @param params {Object} Information about uploaded files.
    * @param callback {Function} Callback to call on function completition.
    */
    addFile: function (projectName, files, params, callback) {
        if (callback === undefined) {
            callback = params;
            params = {};
        }

        var filesInformation = {};

        files.forEach(function (fileName) {
            var index = "files[" + fileName + "]";
            filesInformation[index] = fs.createReadStream(fileName);
        });

        return postApiCallWithFormData('project/' + projectName + '/add-file', extend(filesInformation, params), callback);
    },
    /**
    * Upload latest version of your localization file to Crowdin.
    * @param projectName {String} Should contain the project identifier
    * @param files {Array} Files array that should be updated.
    *   Note! 20 files max are allowed to upload per one time file transfer.
    * @param params {Object} Information about updated files.
    * @param callback {Function} Callback to call on function completition.
    */
    updateFile: function (projectName, files, params, callback) {
        if (callback === undefined) {
            callback = params;
            params = {};
        }

        var filesInformation = {};

        files.forEach(function (fileName) {
            var index = "files[" + fileName + "]";
            filesInformation[index] = fs.createReadStream(fileName);
        });

        return postApiCallWithFormData('project/' + projectName + '/update-file', extend(filesInformation, params), callback);
    },
    /**
    * Delete file from Crowdin project. All the translations will be lost without ability to restore them.
    * @param projectName {String} Should contain the project identifier
    * @param fileName {String} Name of file to delete.
    * @param callback {Function} Callback to call on function completition.
    */
    deleteFile: function (projectName, fileName, callback) {
        return postApiCallWithFormData('project/' + projectName + '/delete-file', { file: fileName }, callback);
    },
    /**
    * Upload existing translations to your Crowdin project
    * @param projectName {String} Should contain the project identifier
    * @param files {Array} Translated files array. Array keys should contain file names in Crowdin.
    *   Note! 20 files max are allowed to upload per one time file transfer.
    * @param language {String} Target language. With a single call it's possible to upload translations for several files but only into one of the languages
    * @param params {Object} Information about updated files.
    * @param callback {Function} Callback to call on function completition.
    */
    updateTranslations: function (projectName, files, language, params, callback) {
        if (callback === undefined) {
            callback = params;
            params = {};
        }

        var filesInformation = {
            language: language
        };

        files.forEach(function (fileName) {
            var index = "files[" + fileName + "]";
            filesInformation[index] = fs.createReadStream(fileName);
        });

        return postApiCallWithFormData('project/' + projectName + '/upload-translation', extend(filesInformation, params), callback);
    },
    /**
    * Track your Crowdin project translation progress by language.
    * @param projectName {String} Should contain the project identifier.
    * @param callback {Function} Callback which returns object with information.
    */
    translationStatus: function (projectName, callback) {
        postApiCall('project/' + projectName + '/status', callback);
    },
    /**
    * Get Crowdin Project details.
    * @param projectName {String} Should contain the project identifier.
    * @param callback {Function} Callback which returns object with information.
    */
    projectInfo: function (projectName, callback) {
        postApiCall('project/' + projectName + '/info', callback);
    },
    /**
    * Download ZIP file with translations. You can choose the language of translation you need.
    */
    downloadTranslations: function (projectName, languageCode) {
        return getApiRequest('project/' + projectName + '/download/' + languageCode + '.zip');
    },
    /**
    * Download ZIP file with all translations.
    */
    downloadAllTranslations: function (projectName) {
        return getApiRequest('project/' + projectName + '/download/all.zip');
    },
    /**
    * Build ZIP archive with the latest translations. Please note that this method can be invoked only once per 30 minutes (there is no such
    * restriction for organization plans). Also API call will be ignored if there were no changes in the project since previous export. 
    * You can see whether ZIP archive with latest translations was actually build by status attribute ("built" or "skipped") returned in response.
    */
    exportTranslations: function (projectName, callback) {
        getApiCall('project/' + projectName + '/export', callback);
    },
    /**
    * Edit Crowdin project
    * @param projectName {String} Name of the project to change
    * @param params {Object} New parameters for the project.
    * @param callback {Function} Callback to call on function completition.
    */
    editProject: function (projectName, params, callback) {
        return postApiCallWithFormData('project/' + projectName + '/edit-project', params, callback);
    },
    /**
    * Delete Crowdin project with all translations.
    * @param projectName {String} Name of the project to delete.
    * @param callback {Function} Callback to call on function completition.
    */
    deleteProject: function (projectName, callback) {
        return postApiCall('project/' + projectName + '/delete-project', callback);
    },
    /**
    * Add directory to Crowdin project.
    * @param projectName {String} Should contain the project identifier.
    * @param directory {String} Directory name (with path if nested directory should be created).
    * @param callback {Function} Callback to call on function completition.
    */
    createDirectory: function (projectName, directory, callback) {
        return postApiCall('project/' + projectName + '/add-directory', { name: directory}, callback);
    },
    /**
    * Rename directory or modify its attributes. When renaming directory the path can not be changed (it means new_name parameter can not contain path, name only).
    * @param projectName {String} Full directory path that should be modified (e.g. /MainPage/AboutUs).
    * @param directory {String} New directory name.
    * @param params {Object} New parameters for the directory.
    * @param callback {Function} Callback to call on function completition.
    */
    changeDirectory: function (projectName, directory, params, callback) {
        return postApiCallWithFormData('project/' + projectName + '/change-directory', { name: directory }, params, callback);
    },
    /**
    * Delete Crowdin project directory. All nested files and directories will be deleted too.
    * @param projectName {String} Should contain the project identifier.
    * @param directory {String} Directory path (or just name if the directory is in root).
    * @param callback {Function} Callback to call on function completition.
    */
    deleteDirectory: function (projectName, directory, callback) {
        return postApiCall('project/' + projectName + '/delete-directory', { name: directory}, callback);
    },
    /**
    * Download Crowdin project glossaries as TBX file.
    */
    downloadGlossary: function (projectName) {
        return getApiRequest('project/' + projectName + '/download-glossary');
    },
    /**
    * Upload your glossaries for Crowdin Project in TBX file format.
    * @param projectName {String} Should contain the project identifier.
    * @param fileNameOrStream {String} Name of the file to upload or stream which contains file to upload.
    * @param callback {Function} Callback to call on function completition.
    */
    uploadGlossary: function (projectName, fileNameOrStream, callback) {
        if (typeof fileNameOrStream === "string") {
            fileNameOrStream = fs.createReadStream(fileNameOrStream);
        }

        return postApiCallWithFormData('project/' + projectName + '/upload-glossary', { file: fileNameOrStream }, callback);
    },
    /**
    * Download Crowdin project Translation Memory as TMX file.
    * @param callback {Function} Callback to call on function completition.
    */
    downloadTranslationMemory: function (projectName, callback) {
        return postApiCall('project/' + projectName + '/download-tm', callback);
    },
    /**
    * Upload your Translation Memory for Crowdin Project in TMX file format.
    * @param projectName {String} Should contain the project identifier.
    * @param fileNameOrStream {String} Name of the file to upload or stream which contains file to upload.
    * @param callback {Function} Callback to call on function completition.
    */
    uploadTranslationMemory: function (projectName, fileNameOrStream, callback) {
        if (typeof fileNameOrStream === "string") {
            fileNameOrStream = fs.createReadStream(fileNameOrStream);
        }

        return postApiCallWithFormData('project/' + projectName + '/upload-tm', { file: fileNameOrStream }, callback);
    },
    /**
    * Get supported languages list with Crowdin codes mapped to locale name and standardized codes.
    * @param callback {Function} Callback to call on function completition.
    */
    supportedLanguages: function (callback) {
        getApiCall('supported-languages', callback);
    }
};
