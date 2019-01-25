//menu item click handler d

function activeMenuItem (event) {
  var menuParent=event.target.parentNode
  var classStyle=menuParent.getAttribute('class')
  menuParent.setAttribute('class', 'app-head-menu-item-active' + ' ' + classStyle)
}

function activeHeadMenuByPath(menuPath,menu_id)
{
  var menuItem=document.getElementById(menu_id)
  var menuLabel=menuItem.getAttribute('label')
  if(menuPath.indexOf(menuLabel))
  {
    var classStyle=menuItem.getAttribute('class')
    menuItem.setAttribute('class','app-head-menu-item-active' + ' '+classStyle)
  }
}

export {
  activeMenuItem,
  activeHeadMenuByPath
}
