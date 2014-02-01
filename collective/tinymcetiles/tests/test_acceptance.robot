*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  Selenium2Screenshots/keywords.robot
Library   collective.tinymcetiles.tests.test_acceptance.Keywords

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***
${SLEEP}  3.5s


*** Test Cases ***

Scenario: As an editor I can inset a "DummyTile" in a document
    Given a site owner
      and a new document
     When I insert a "DummyTile" in a document
     Then a visitor can view "Test tile rendered"

Del Boy opens a chippie using tiles
    narrate "Del Boy has a great idea to open a fish and chip shop"
    narrate "Now he needs a website"
    narrate "Luckily his friend rodney got him this great Plone site"
    narrate "Now he can put is food menu online in no time!"
    narrate "He logs in"
    Given a site owner
    click link  Home
    click add new
    show pointy note  css=a.contenttype-document
    ...    First he creates a new page
    show pointy note  css=dl#plone-contentmenu-factories dd.actionMenuContent
    ...    note the add new menu no longer includes folder or collection
    add new page
    with the label  Title  input text  Menus
    with the label  Summary  input text  "only fools and chips" takeaway menu
    visual edit "We strive to make the best fish and chips your unemployment benefit can buy"

    #uploads a pic the shop.
    upload image  http://images.smh.com.au/2012/01/20/2905552/MJtravelwide6_20120120132625161061-420x0.jpg

    click button  Save

    narrate "The image is stored in the page, no need to create a folder"
    show pointy note  css=dl#plone-contentmenu-factories dd.actionMenuContent
    ...    note the display menu is gone

    narrate "Now he needs to add his menu items"
    narrate "We can just add a page within a page"
    narrate "No fiddling with Folders or default page display settings"

    click add new
    add new page
    with the label  Title  input text  Fish
    with the label  Summary  input text  Cod dipped in fat

    upload image  http://www.messersmith.name/wordpress/wp-content/uploads/2009/11/titan_triggerfish_balistoides_viridescens_P7290834.jpg
    click button  Save
    click link  Menus

    narrate "Now we wants to list his menu"

    click link  Edit
    #adds "The chippie menu" sub title and then clicks "add tile" button.
    narrate "Del is lazy so he wants an automated listing"

 #   insert tile "Content listing"
    show pointy note  css=.mce_plonetiles
    ...   We can insert a tile to do this
    Click link  css=.mce_plonetiles
    select frame  css=.plonepopup iframe
    ${n}=  label "Content listing"
    show pointy note  ${n}  "Content listing tiles replaces collections"
    with the label  Content listing  select checkbox
    show pointy note  css=.criteria
    ...     The default query lists the local context
    ${n}=  label "Display mode"
    show pointy note  ${n}  "He can choose how he wants it displayed"
    select from list by label  ${n}  Summary view
    click button  Create

    In the editor he sees a shortcode and a preview of what the listing will look like (hopefully)
    he clicks save and views the page which includes the fish, description and thumbnail of the fish image
    now he wants to extend his menu. he adds new page called "chips".
    enters chips description and uploads pic of chips.
    clicks back up to "menu" page and shows that chips automatically got added to the menu listing



*** Keywords ***

show pointy note
    [arguments]     ${locator}  ${note}
    ${n} =  add pointy note  ${locator}
    ...    ${note}
    ...    position=left
    sleep  ${SLEEP}
    Remove element  ${n}


click add new
    Click link  css=dl#plone-contentmenu-factories dt.actionMenuHeader a

add new page
    Click link  css=a#document

visual edit "${text}"
    select frame  id=text_ifr
    Input text  id=content  ${text}
    unselect frame
    # see http://stackoverflow.com/questions/17306305/how-to-select-the-text-of-a-tinymce-field-with-robot-framework-and-selenium2libr

upload image
    [arguments]     ${url}
    click link  css=#text_image
    select frame  css=.plonepopup iframe
    #click link  External
    #input text  css=#imageurl  ${url}
    ${file}=  download file  ${url}
    click link  upload
    choose file  id=uploadfile  ${file}
    click button  Upload
    select from list by label  classes  Right
    select from list by label  dimensions  Mini (200x200)
    sleep   1s
    click button  OK


Narrate "${text}"
    ${note1} =  Add note  css=body
    ...  ${text}
    sleep  ${SLEEP}
    Remove element  ${note1}

# Given

A site owner
  Log in  ${SITE_OWNER_NAME}  ${SITE_OWNER_PASSWORD}

A new document
  Enable autologin as  Manager
  Set autologin username  ${SITE_OWNER_NAME}
  Create content  type=Document
  ...  id=a-document  title=A New Document
  Disable autologin

# When

When I insert a "DummyTile" in a document
  Go to  ${PLONE_URL}/a-document/edit
#    Select Frame  pools_to_register_iframe
  insert tile "Dummy tile"
  # still editing in tinymce
  click button  Save

insert tile "${tile}"
  element should be visible  css=.mceLayout .mceToolbar
  Click link  css=.mce_plonetiles
  page should contain  ${tile}
  select frame  css=.plonepopup iframe
#  element should be visible  css=form#add-tile
  with the label  ${tile}  select checkbox
  click button  Create
#  page should contain  img
#  element should be visible css=img.mceTile
  click button  Save


# Then

A visitor can view "${text}"
  wait until page contains  ${text}
#  Log out
#  Go to  ${PLONE_URL}/a-document
#  Page should contain  Test tile rendered


With the label
    [arguments]     ${title}   ${extra_keyword}   @{list}
    ${for}=  label "${title}"
    Run Keyword     ${extra_keyword}  id=${for}   @{list}

label "${title}"
    [Return]  ${for}
    ${for}=  Get Element Attribute  xpath=//label[contains(., "${title}")]@for

