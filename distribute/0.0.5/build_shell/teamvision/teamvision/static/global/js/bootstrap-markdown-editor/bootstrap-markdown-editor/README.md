# Bootstrap Markdown Editor

[![Built with Grunt](https://cdn.gruntjs.com/builtwith.png)](http://gruntjs.com/)

Markdown editor for Bootstrap with preview, image upload support, shortcuts and other features.  
This is a jQuery plugin.

**Demo**: http://inacho.github.io/bootstrap-markdown-editor/

## Requirements

* Bootstrap 3
* jQuery
* Ace editor (http://ace.c9.io)

## Features

* Preview support
* Image upload support (drag and drop & button)
* Shortcuts
* Multiples instances on the same page
* Fullscreen
* Themes
* i18n

## Screenshot

![Screenshot 1](screenshots/screenshot-01.png)

## Installation with Bower

    bower install bootstrap-markdown-editor --save

## Example Usage

Include the CSS files of Bootstrap and Bootstrap Markdown Editor:

```html
<link href="bower_components/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="bower_components/bootstrap-markdown-editor/dist/css/bootstrap-markdown-editor.css" rel="stylesheet">
```

Include the scripts of jQuery, Ace and Bootstrap Markdown Editor.
Optionally, include the script of Bootstrap to enable tooltips:

```html
<script src="bower_components/jquery/dist/jquery.min.js"></script>
<script src="bower_components/bootstrap/dist/js/bootstrap.min.js"></script>
<script src="bower_components/ace-builds/src-min/ace.js"></script>
<script src="bower_components/bootstrap-markdown-editor/dist/js/bootstrap-markdown-editor.js"></script>
```

Create a textarea for the editor with optional content in markdown format:

```html
<textarea name="text" id="myEditor"># Test</textarea>
```

Initialize the editor:

```javascript
$('#myEditor').markdownEditor();
```

## Implementing the preview

You have to implement the parsing of the Markdown.  
Bootstrap Markdown Editor provides you a callback where you have to parse the markdown and return the html.  
To activate the preview you have to use the following options:

```javascript
$('#myEditor').markdownEditor({
  // Activate the preview:
  preview: true,
  // This callback is called when the user click on the preview button:
  onPreview: function (content, callback) {

    // Example of implementation with ajax:
    $.ajax({
      url: 'preview.php',
      type: 'POST',
      dataType: 'html',
      data: {content: content},
    })
    .done(function(result) {
      // Return the html:
      callback(result);
    });

  }
});
```

## Implementing the image upload

You have to implement the server side part of the upload process.  
To activate the image uploads you have to use the following options:

```javascript
$('#myEditor').markdownEditor({
  imageUpload: true, // Activate the option
  uploadPath: 'upload.php' // Path of the server side script that receive the files
});
```

In your server side script you have to return an array of the **public path** of the successfully uploaded images in json format.

Example in PHP:

```php
$uploadedFiles = array();

if (! empty($_FILES)) {
  foreach ($_FILES as $file) {
    if (superAwesomeUploadFunction($file)) {
      $uploadedFiles[] = '/img/' . urlencode($file['name']);
    }
  }
}

echo json_encode($uploadedFiles);
```

Response example:

```
["/path/to/my-picture.jpg"]
```

## Shortcuts

The following shortcuts are available.  
They can be used with or without selected text.

- **Ctrl-B / ⌘B**: Bold
- **Ctrl-I / ⌘I**: Italic
- **Ctrl-K / ⌘K**: Link

## Plugin documentation

### Options

The following options can be passed as an object at the initialization of the plugin:

```javascript
$('#myEditor').markdownEditor({
  // Options
});
```

Also, you can override the plugin default options. Example:

```javascript
$.fn.markdownEditor.defaults.width = '250px';
```

#### width

**Type**: string  
**Default**: '100%'

The width of the editor

#### height

**Type**: string  
**Default**: '400px'

The height of the editor

#### fontSize

**Type**: string  
**Default**: '14px'

The font size of the editor

#### theme

**Type**: string  
**Default**: 'tomorrow'

The theme of the editor. See the available themes at the homepage of Ace (http://ace.c9.io)

#### softTabs

**Type**: boolean  
**Default**: true

Pass false to disable the use of soft tabs. Soft tabs means you're using spaces instead of the tab character ('\t')

#### fullscreen

**Type**: boolean  
**Default**: true

Enable / disable fullscreen

#### imageUpload

**Type**: boolean  
**Default**: false

Enable / disable the upload of images. If enabled, you have to specify the option `uploadPath`

#### uploadPath

**Type**: uploadPath  
**Default**: ''

The path of the server side script that receives the images. The script has to return an array of the **public path** of the successfully uploaded images in json format.

#### preview

**Type**: boolean  
**Default**: false

Enable / disable the preview. If enabled, you have to specify the option `onPreview`

#### onPreview

**Type**: function  
**Default**:

```javascript
function (content, callback) {
  callback(content);
}
```

This callback is called when the user clicks on the preview button and has two parameters:  
**content** that contains the text in markdown.  
**callback** is function that you have to call with the parsed html as a parameter

#### label

**Type**: object
**Default**:

```javascript
{
  btnHeader1: 'Header 1',
  btnHeader2: 'Header 2',
  btnHeader3: 'Header 3',
  btnBold: 'Bold',
  btnItalic: 'Italic',
  btnList: 'Unordered list',
  btnOrderedList: 'Ordered list',
  btnLink: 'Link',
  btnImage: 'Insert image',
  btnUpload: 'Uplaod image',
  btnEdit: 'Edit',
  btnPreview: 'Preview',
  btnFullscreen: 'Fullscreen',
  loading: 'Loading'
}
```

This object contains the strings that can be translated

### Methods

The methods are invoked passing the name of the method as string.  

```javascript
var content = $('#myEditor').markdownEditor('content'); // Returns the content of the editor
$('#myEditor').markdownEditor('setContent', content); // Sets the content of the editor
```

## License

Licensed under MIT (https://github.com/inacho/bootstrap-markdown-editor/blob/master/LICENSE).

## Authors

[Ignacio de Tomás](https://github.com/inacho)
