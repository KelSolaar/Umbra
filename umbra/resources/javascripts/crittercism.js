// crittercismClientLibrary.js
// Load this file into the page where you want to use Crittercism.

var Crittercism = (function() {
	var isUnderTest = function() {
		return typeof inTest !== 'undefined';
	}
	
  // Some constants
	var LIB_VERSION							= 'pre';
  var LS_APP_STATE						= "Crittercism.app_state";
  var LS_DID        					= "Crittercism.did";
  var LS_LAST_SEEN						= "Crittercism.last_seen";
  var LS_BREADCRUMBS					= 'Crittercism.breadcrumbs';
  var SESSION_LENGTH_MS				= 30 * 60 * 1000;				// 30 mins in msec
  // Send 3 handled exceptions/minute
  var HANDLED_EXCEPTION_TRANSMISSION_INTERVAL_MSEC = 20 * 1000;
  // How many handled exceptions can we enqueue before we start dropping them?
  var MAX_ENQUEUED_HANDLED_EXCEPTIONS = 20;
  
  var handledExceptionsTally	= 0;
  
	// appId holds the alphanumeric token Crittercism uses to identify the app
	var appId							= null;
	var iframeSrc					= null;
	var initialized				= false;
	
	var hasHTML5Storage = function() {
    try {
      return 'localStorage' in window && window['localStorage'] !== null;
    } catch (e) {
      return false;
    }
	};
	
	/*
	 * Sessions
	 */
	// newSession method marks session start; returns true if this is a "new session",
	// otherwise returns false.
	var isNewSession = function() {
		if(hasHTML5Storage()) {			
      var lastSeenDate = getLastSeenDate();
      
      if(lastSeenDate) {
      	var now = new Date();
      	var lastSeenAgoMs = now - lastSeenDate;
      	
      	return lastSeenAgoMs >= SESSION_LENGTH_MS ? true : false;
      } else {
      	// No recorded last session, return true (is new session)
      	return true;
      }   
		} else {
			// No storage, return app load on every page. Should be rare.
			return true;
		}
	};
	
	var markSeen = function() {
		if(hasHTML5Storage()) {
			localStorage[LS_LAST_SEEN] = new Date().toString();
		}
	};
	
	var getLastSeenDate = function() {
		var lastSessionStartString = localStorage.getItem(LS_LAST_SEEN);
		
		if(lastSessionStartString) {
			try {
				return new Date(lastSessionStartString);
			} catch(e) {
				return null;
			}
		} else {
			return null;
		}
	};
	
	/* 
	 * Device ID getter/setter
	 */
	var getDeviceId = function() {
		if(hasHTML5Storage()) {
			try {
				return localStorage.getItem(LS_DID);
	    } catch(e) {
	    	return '';
	    }
		} else {
			return '';
		}
	};

	var setDeviceId = function(did) {
		if(hasHTML5Storage()) {
			localStorage.setItem(LS_DID, did);
	  }
	};
	
	/*
	 * IFRAME initialization / communication routines
	 */
	var crittercismContentWindow	= null;			// used for cross-domain communication
	var communicationReady				= false;		// Can we send data to the iframe yet?
	var messageQueue							= [];				// Only used if we aren't ready to send
	var crashesRecorded						= 0;
	
	// Inject the iframe into the root of the document, if needed.
	var injectIframe = function() {
		if(document.getElementById('critterframe') == null) {
			var critterFrame						= document.createElement('iframe');
			critterFrame.id							= 'critterframe';
			critterFrame.src						= iframeSrc;
			critterFrame.style.display 	= 'none';
			
			document.body.appendChild(critterFrame);
		}
	};
	
	// Try to send a message to the iframe.
	// If we can't send, queue up for later.
	var sendMessage = function(message) {
		if(communicationReady) {
			crittercismContentWindow.postMessage(message, '*');
		} else {
			messageQueue.push(message);
		}
	};
	
	// Take all messages from the queue and send them.
	// Not called unless we get messages in queue, which doesn't usually happen.
	var drainQueue = function() {
		while(message = messageQueue.pop()) {
			crittercismContentWindow.postMessage(message, '*');
		}
	};
	
	// Call when communication established btw client and server (iframe)
	// Sets communication ready flag, drains the queue.
	var setCommunicationReady = function() {
		communicationReady = true;
		drainQueue();
	};
	
	// Handles messages sent back from the iframe. Convention: data looks like
	// { "type": "MesssageType",
	//   "contents": { ... Parameterized on type ... }
	// }
	var iframeMessageHandler = function(event) {
		// TODO: Re-enable security checks
		//if(event.origin == "https://api.crittercism.com") {
			// Use a two-way SYN/ACK-like initialization procedure
			switch(event.data.type) {
				case 'iframeSyn':
					crittercismContentWindow	= event.source;
					crittercismContentWindow.postMessage({ type: 'clientSynAck' }, "*");
					break;
					
				case 'iframeSynAck':
					crittercismContentWindow	= event.source;
					crittercismContentWindow.postMessage({ type: 'clientAck' }, "*");
					setCommunicationReady();
					break;
					
				case 'iframeAck':
					setCommunicationReady();
					break;
					
				case 'setDeviceId':
					setDeviceId(event.data.contents.deviceId);
					break;
					
				default:
					// Ignore unrecognized message types
					break;
			}
		//}
	};
	
	if(!isUnderTest()) {
		// Have to explicitly check for tests because this code will run before any of our specs
		// and mess stuff up if it does...avoiding this anti-pattern in the future.
		window.addEventListener("message", iframeMessageHandler, false);
	}
	
	// We'll probably load before the iframe, but not 100% guaranteed.
	// Do a little SYN/ACK dance with the iframe here to be sure.
	if(document.getElementById("crittercism_iframe")) {
		// iframe was ready first -- we lost the race. Uncommon.
		crittercismContentWindow = document.getElementById("crittercism_iframe");
		// TODO: Remove "*"
		crittercismContentWindow.postMessage({ type: "clientSyn" }, "*");
	}
	
	/*
	 * End of IFRAME communication / init routines
	 */
	
	/*
	 * Stack trace stuff starts here
	 */
	
  // Domain Public by Eric Wendelin http://eriwen.com/ (2008)
  //                  Luke Smith http://lucassmith.name/ (2008)
  //                  Loic Dachary <loic@dachary.org> (2008)
  //                  Johan Euphrosine <proppy@aminche.com> (2008)
  //                  Oyvind Sean Kinsey http://kinsey.no/blog (2010)
  //                  Victor Homyakov <victor-homyakov@users.sourceforge.net> (2010)
  /**
   * Main function giving a function stack trace with a forced or passed in Error
   *
   * @cfg {Error} e The error to create a stacktrace from (optional)
   * @cfg {Boolean} guess If we should try to resolve the names of anonymous functions
   * @return {Array} of Strings with functions, lines, files, and arguments where possible
   */
  function printStackTrace(options) {
      options = options || {guess: true};
      var ex = options.e || null, guess = !!options.guess;
      var p = new printStackTrace.implementation(), result = p.run(ex);
      return (guess) ? p.guessAnonymousFunctions(result) : result;
  }
  printStackTrace.implementation=function(){};printStackTrace.implementation.prototype={run:function(ex,mode){ex=ex||this.createException();mode=mode||this.mode(ex);if(mode==='other'){return this.other(arguments.callee);}else{return this[mode](ex);}},createException:function(){try{this.undef();}catch(e){return e;}},mode:function(e){if(e['arguments']&&e.stack){return'chrome';}else if(typeof e.message==='string'&&typeof window!=='undefined'&&window.opera){if(!e.stacktrace){return'opera9';}if(e.message.indexOf('\n')>-1&&e.message.split('\n').length>e.stacktrace.split('\n').length){return'opera9';}if(!e.stack){return'opera10a';}if(e.stacktrace.indexOf("called from line")<0){return'opera10b';}return'opera11';}else if(e.stack){return'firefox';}return'other';},instrumentFunction:function(context,functionName,callback){context=context||window;var original=context[functionName];context[functionName]=function instrumented(){callback.call(this,printStackTrace().slice(4));return context[functionName]._instrumented.apply(this,arguments);};context[functionName]._instrumented=original;},deinstrumentFunction:function(context,functionName){if(context[functionName].constructor===Function&&context[functionName]._instrumented&&context[functionName]._instrumented.constructor===Function){context[functionName]=context[functionName]._instrumented;}},chrome:function(e){var stack=(e.stack+'\n').replace(/^\S[^\(]+?[\n$]/gm,'').replace(/^\s+(at eval )?at\s+/gm,'').replace(/^([^\(]+?)([\n$])/gm,'{anonymous}()@$1$2').replace(/^Object.<anonymous>\s*\(([^\)]+)\)/gm,'{anonymous}()@$1').split('\n');stack.pop();return stack;},firefox:function(e){return e.stack.replace(/(?:\n@:0)?\s+$/m,'').replace(/^\(/gm,'{anonymous}(').split('\n');},opera11:function(e){var ANON='{anonymous}',lineRE=/^.*line (\d+), column (\d+)(?: in (.+))? in (\S+):$/;var lines=e.stacktrace.split('\n'),result=[];for(var i=0,len=lines.length;i<len;i+=2){var match=lineRE.exec(lines[i]);if(match){var location=match[4]+':'+match[1]+':'+match[2];var fnName=match[3]||"global code";fnName=fnName.replace(/<anonymous function: (\S+)>/,"$1").replace(/<anonymous function>/,ANON);result.push(fnName+'@'+location+' -- '+lines[i+1].replace(/^\s+/,''));}}return result;},opera10b:function(e){var lineRE=/^(.*)@(.+):(\d+)$/;var lines=e.stacktrace.split('\n'),result=[];for(var i=0,len=lines.length;i<len;i++){var match=lineRE.exec(lines[i]);if(match){var fnName=match[1]?(match[1]+'()'):"global code";result.push(fnName+'@'+match[2]+':'+match[3]);}}return result;},opera10a:function(e){var ANON='{anonymous}',lineRE=/Line (\d+).*script (?:in )?(\S+)(?:: In function (\S+))?$/i;var lines=e.stacktrace.split('\n'),result=[];for(var i=0,len=lines.length;i<len;i+=2){var match=lineRE.exec(lines[i]);if(match){var fnName=match[3]||ANON;result.push(fnName+'()@'+match[2]+':'+match[1]+' -- '+lines[i+1].replace(/^\s+/,''));}}return result;},opera9:function(e){var ANON='{anonymous}',lineRE=/Line (\d+).*script (?:in )?(\S+)/i;var lines=e.message.split('\n'),result=[];for(var i=2,len=lines.length;i<len;i+=2){var match=lineRE.exec(lines[i]);if(match){result.push(ANON+'()@'+match[2]+':'+match[1]+' -- '+lines[i+1].replace(/^\s+/,''));}}return result;},other:function(curr){var ANON='{anonymous}',fnRE=/function\s*([\w\-$]+)?\s*\(/i,stack=[],fn,args,maxStackSize=10;while(curr&&curr['arguments']&&stack.length<maxStackSize){fn=fnRE.test(curr.toString())?RegExp.$1||ANON:ANON;args=Array.prototype.slice.call(curr['arguments']||[]);stack[stack.length]=fn+'('+this.stringifyArguments(args)+')';curr=curr.caller;}return stack;},stringifyArguments:function(args){var result=[];var slice=Array.prototype.slice;for(var i=0;i<args.length;++i){var arg=args[i];if(arg===undefined){result[i]='undefined';}else if(arg===null){result[i]='null';}else if(arg.constructor){if(arg.constructor===Array){if(arg.length<3){result[i]='['+this.stringifyArguments(arg)+']';}else{result[i]='['+this.stringifyArguments(slice.call(arg,0,1))+'...'+this.stringifyArguments(slice.call(arg,-1))+']';}}else if(arg.constructor===Object){result[i]='#object';}else if(arg.constructor===Function){result[i]='#function';}else if(arg.constructor===String){result[i]='"'+arg+'"';}else if(arg.constructor===Number){result[i]=arg;}}}return result.join(',');},sourceCache:{},ajax:function(url){var req=this.createXMLHTTPObject();if(req){try{req.open('GET',url,false);req.send(null);return req.responseText;}catch(e){}}return'';},createXMLHTTPObject:function(){var xmlhttp,XMLHttpFactories=[function(){return new XMLHttpRequest();},function(){return new ActiveXObject('Msxml2.XMLHTTP');},function(){return new ActiveXObject('Msxml3.XMLHTTP');},function(){return new ActiveXObject('Microsoft.XMLHTTP');}];for(var i=0;i<XMLHttpFactories.length;i++){try{xmlhttp=XMLHttpFactories[i]();this.createXMLHTTPObject=XMLHttpFactories[i];return xmlhttp;}catch(e){}}},isSameDomain:function(url){return typeof location!=="undefined"&&url.indexOf(location.hostname)!==-1;},getSource:function(url){if(!(url in this.sourceCache)){this.sourceCache[url]=this.ajax(url).split('\n');}return this.sourceCache[url];},guessAnonymousFunctions:function(stack){for(var i=0;i<stack.length;++i){var reStack=/\{anonymous\}\(.*\)@(.*)/,reRef=/^(.*?)(?::(\d+))(?::(\d+))?(?: -- .+)?$/,frame=stack[i],ref=reStack.exec(frame);if(ref){var m=reRef.exec(ref[1]);if(m){var file=m[1],lineno=m[2],charno=m[3]||0;if(file&&this.isSameDomain(file)&&lineno){var functionName=this.guessAnonymousFunction(file,lineno,charno);stack[i]=frame.replace('{anonymous}',functionName);}}}}return stack;},guessAnonymousFunction:function(url,lineNo,charNo){var ret;try{ret=this.findFunctionName(this.getSource(url),lineNo);}catch(e){ret='getSource failed with url: '+url+', exception: '+e.toString();}return ret;},findFunctionName:function(source,lineNo){var reFunctionDeclaration=/function\s+([^(]*?)\s*\(([^)]*)\)/;var reFunctionExpression=/['"]?([0-9A-Za-z_]+)['"]?\s*[:=]\s*function\b/;var reFunctionEvaluation=/['"]?([0-9A-Za-z_]+)['"]?\s*[:=]\s*(?:eval|new Function)\b/;var code="",line,maxLines=Math.min(lineNo,20),m,commentPos;for(var i=0;i<maxLines;++i){line=source[lineNo-i-1];commentPos=line.indexOf('//');if(commentPos>=0){line=line.substr(0,commentPos);}if(line){code=line+code;m=reFunctionExpression.exec(code);if(m&&m[1]){return m[1];}m=reFunctionDeclaration.exec(code);if(m&&m[1]){return m[1];}m=reFunctionEvaluation.exec(code);if(m&&m[1]){return m[1];}}}return'(?)';}};
  /****** end public domain *****/
  
  var cleanStackTrace = function(stack) {
    var cleanStack = [];
    var regexFilters = [/^crittercismErrorHandler/i, /^printStackTrace/i];
    for (var i = 0, l = stack.length; i < l; i++) {
        var line = stack[i];
        
        var filter = false;
        // run against regex filters, break if doesnt match
        for (var j = 0, r = regexFilters.length; j < r; j++) {
            if(line.match(regexFilters[j])) {
                filter = true;
                break;
            }
        }
        if(!filter) {
            cleanStack.push(line);
        }
    }
    return cleanStack;
  }
  
  /*
   * End stack trace stuff here
   */
  
  /*
   * App state
   */
  var appVersion;
  var appState			= {
  		metadata:		{}
  };
  
  var appLoadSent		= false;
  
  var isNullOrEmpty = function(val) {
    return (typeof(val) == 'undefined' || val == null || val == '');
  };
  
  var setAppState = function(key, value) {
    if(hasHTML5Storage()) {
        state = getAppState();
        state[key] = value;
        localStorage.setItem(LS_APP_STATE, state);
    } else {
        appState[key] = value;
    }
  };

  var getBatteryLevel = function() {
    battery = null;
    // fragmentation ftw
    if(navigator.battery) {
        battery = navigator.battery.level;
    } else if(navigator.mozBattery) {
        battery = navigator.mozBattery.level;
    } else if(navigator.webkitBattery) {
        battery = navigator.webkitBattery.level;
    } 
    return battery;
	};
  
  var getLocalStorageSize = function() {
  	var size = 0;
    
  	// times 2 b/c UTF-16 strings take two bytes each
  	for (var i = 0; i < localStorage.length; i++){
  		var tmpKey = localStorage.key(i);
      size += tmpKey.length*2;
      if(!isNullOrEmpty(localStorage.getItem(tmpKey))) {
      	size += localStorage.getItem(localStorage.key(i)).length*2;
      }
    }
    
    return size;
  };
  
  var sendMetadata = function() {
  	sendMessage({"type": "metadata", "contents": {
    	app_id:						appId,
    	device_id:				getDeviceId(),						// Device ID
	  	library_version:	LIB_VERSION,
	  	device_name:			'html5',									// Clean up later
    	metadata: 				appState['metadata']
    }});
  };
  
  // Internal getter -- usually use getCurrentState.
  var getAppState = function() {
  	if(hasHTML5Storage()) {
  		try {
  			return JSON.parse(localStorage.getItem(LS_APP_STATE)) || {};
  		} catch(e) {
  			return (appState || {});
  		}
  	} else {
  		return (appState || {});
  	}
  };
  
  var getCurrentState = function() {
    var deviceApplicationState = getAppState();
    if(hasHTML5Storage()) {
        appState['local_storage'] = getLocalStorageSize();
    }
    
    var batteryLevel = getBatteryLevel();
    if(batteryLevel) {
    	deviceApplicationState['battery_level'] = getBatteryLevel();
    }
    
    deviceApplicationState['app_version']		= appVersion;
    
    return deviceApplicationState;
  };
  
  /*
   * Install event handlers
   */
  var crittercismErrorHandler = function(errorMsg, url, lineNumber) {
  	++crashesRecorded;
    var stack = cleanStackTrace(printStackTrace({e:errorMsg, guess: true}));
    sendMessage({type:'crash',
    	contents: {
    		app_id:										appId,
    		app_state:								getCurrentState(),
				breadcrumbs:							breadcrumbs,
    		did:											getDeviceId(),						// Device ID
    		exception_name:						'Error',
    		exception_reason:					errorMsg,
    		library_version:					LIB_VERSION,
    		unsymbolized_stacktrace:	stack }
    });
    
    return true;
  };
  
  // Register ourselves for onload event (unhandled exception)
  window.onerror = crittercismErrorHandler;
  
  var breadcrumbs = (function() {
  	if(hasHTML5Storage()) {
  		var breadcrumbJson 			= localStorage.getItem(LS_BREADCRUMBS) || "[]";
  		var previousBreadcrumbs	= JSON.parse(breadcrumbJson);
  	} else {
  		var previousBreadcrumbs = [];
  	}
  	
  	return {
  		"current_session": [],
  		"previous_session": previousBreadcrumbs
  	};
  })();
  
  // Returns ISO-formatted DateTime, used because controller methods on server
  // expect ISO datetime in passed breadcrumbs
  var getNowISODateString = function () {
  	var d = new Date();
    
    function pad(n) {
        return n<10 ? '0'+n : n
    }
    
    return d.getUTCFullYear()+'-'
            + pad(d.getUTCMonth()+1)+'-'
            + pad(d.getUTCDate())+'T'
            + pad(d.getUTCHours())+':'
            + pad(d.getUTCMinutes())+':'
            + pad(d.getUTCSeconds())+'Z'
  };
  
  /*
   * Handled exceptions 
   */
  
  var handledExceptionQueue = [];			// Not going to preserve these between sessions
  var exceptionSendTimer		= null;
  var lastRunQueueLength		= MAX_ENQUEUED_HANDLED_EXCEPTIONS + 1;
  var thisRunQueueLength		= null;
  
  // Place a handled exception into the handled exceptions queue, but don't send it yet.
  // Sending is triggered by a call to sendHandledExceptions.
  var enqueueHandledException = function(err) {
  	if(handledExceptionQueue.length < MAX_ENQUEUED_HANDLED_EXCEPTIONS) {
    	var scrubbedErr = {
    			name:			(err && (typeof err.name == 'string')) ? err.name : 
    				"Unknown Exception (No name passed by caller)",
    			message:	(err && (typeof err.message == 'string')) ? err.message :
    				"Unknown Exception Reason (No reason passed by caller)"
    	};
    	
      var stack = cleanStackTrace(
      		printStackTrace({
      				e: 			scrubbedErr.message,
		      		guess: 	true
		      	}
      		)
      );
      
      var message = { type: 'handled_exception',
      		contents: {
	      		app_id: 						appId,
	      		hashed_device_id:		getDeviceId(),
				  	library_version:		LIB_VERSION,
				  	exceptions:					[ { library_version: LIB_VERSION,
				  		exception_name:						scrubbedErr.name,
			    		exception_reason:					scrubbedErr.message,
			    		library_version:					LIB_VERSION,
			    		state:										getCurrentState(),
			    		unsymbolized_stacktrace:	stack
			    		}
				  	]
      		}
      };
  	
      handledExceptionQueue.push(message);
  	}
  	
  	return this;
  };
  
  var sendHandledExceptions = function() {
		var exceptionSender = function() {
			thisRunQueueLength = handledExceptionQueue.length;
		
			if(thisRunQueueLength > 0) {
				sendMessage(handledExceptionQueue.pop());
			}
		
			if(thisRunQueueLength != 0 || lastRunQueueLength != 0) {
				exceptionSendTimer = window.setTimeout(exceptionSender, HANDLED_EXCEPTION_TRANSMISSION_INTERVAL_MSEC);
			} else {
				exceptionSendTimer = null;
			}
			
			lastRunQueueLength = thisRunQueueLength;
		};
		
		if(exceptionSendTimer == null) {
			exceptionSender();
		}
  };
  	
	// Public interface starts here
	// TODO: Document parameters
	return {
		init: function(options) {
			initialized	= true;
			appId 			= options['appId'];
			appVersion 	= options['appVersion']		|| 'unspecified';
			
			// Debugging hook for overriding where we get the iframe.
			iframeSrc		= options['_iframeSrc']  	|| 'http://api.crittercism.com/html5-static/html/iframe.html';
			
			injectIframe();
			if(appLoadSent == false && isNewSession()) {
			  sendMessage({type: 'appLoad', contents: {
			  	app_id:						appId,
			  	did:							getDeviceId(),						// Device ID
			  	library_version:	LIB_VERSION,
			  	app_state:				getCurrentState()}} );
			  appLoadSent = true;
			}
			
			markSeen();
			return this;
		},
		
		// Bulk reset of user-supplied metadata.
    setMetadata: function(userMetadata) {
    	if(initialized) {
	    	// We don't blow out the username, so if userMetadata doesn't have one but appState
	    	// does, preserve the one in appState.
	    	if(appState['metadata']['username'] && isNullOrEmpty(userMetadata['username'])) {
	    		userMetadata['username'] = appState['metadata']['username']; 
	    	}
	
	      appState['metadata'] = userMetadata;		// Save metadata here
	      sendMetadata();
    	} else {
    		throw new Error("Crittercism.init call required before setMetadata");
    	}
      
      markSeen();
      return this;			// Support fluent syntax
    },
    
    setValue: function(key, value) {
    	if(initialized) {
	    	if(!isNullOrEmpty(key)) {
	    		appState['metadata'][key] = value;
	    	}
	    	
	    	sendMetadata();
    	} else {
    		throw new Error("Crittercism.init call required before setValue");
    	}
    	
    	markSeen();
    	return this;
    },
    
    setUsername: function(username) {
    	if(initialized) {
    		appState['metadata']['username'] = username;
    	} else {
    		throw new Error("Crittercism.init call required before setUsername");
    	}
    	
    	markSeen();
    	return this;
    },

    // Assumption that we're passing an Error object into logHandledException, or something
    // with a "name" and "message" property
    logHandledException: function(err) {
    	if(initialized) {
	    	enqueueHandledException(err);
	    	sendHandledExceptions();
    	} else {
    		throw new Error("Crittercism.init call required before logHandledException");
    	}
    	
    	markSeen();
    	return this;
    },

	logExternalException : function(errorMsg, url, lineNumber, stack) {
		 sendMessage( {
		 			type:'crash',
		    		contents: {
			    		app_id:	appId,
			    		app_state: getCurrentState(),
						breadcrumbs: breadcrumbs,
			    		did: getDeviceId(),
			    		exception_name: 'Error',
			    		exception_reason: errorMsg,
			    		library_version: LIB_VERSION,
			    		unsymbolized_stacktrace: stack
			    		}
		});
	},
		   
    leaveBreadcrumb: function(crumb) {
    	if(initialized) {
	    	if(typeof crumb == 'string') {
	    		// record the breadcrumb
	    		breadcrumbs['current_session'].push([ crumb , getNowISODateString() ]);
	    		
	    		if(hasHTML5Storage()) {
	    			localStorage[LS_BREADCRUMBS] = JSON.stringify(breadcrumbs['current_session']);
	    		}
	    	} else {
	    		throw new Error("Invalid breadcrumb type; must be a string");
	    	}
    	} else {
    		throw new Error("Crittercism.init call required before leaveBreadcrumb");
    	}
    	
    	markSeen();
    	return this;
    },
    
    // For debugging (not used in normal operation)
    _dumpState: function() {
			return {
				appId:									appId,
				appState:								appState,
				breadcrumbs:						breadcrumbs,
				communicationReady: 		communicationReady,
				crashesRecorded:				crashesRecorded,
				messageQueue:						messageQueue.slice(),
				lastSeen:								getLastSeenDate(),
				handledExceptionQueue:	handledExceptionQueue,
				exceptionSendTimer:			exceptionSendTimer
			};
		},
		
		_reset: function() {
			appId								= false;
			communicationReady	= false;
			appLoadSent					= false;
			appState						= {};
			messageQueue				= [];
		},
		
		_crashesRecorded: function() {
			return crashesRecorded;
		},
		
		_resetQueues: function() {
			messageQueue					= [];
			handledExceptionQueue = [];
		}
	};
})();
