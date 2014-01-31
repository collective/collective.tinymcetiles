*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  Selenium2Screenshots/keywords.robot

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
    ${n} =  add pointy note  css=a.contenttype-document
    ...    First he creates a new page
    ...    position=left
    sleep  ${SLEEP}
    Remove element  ${n}
    ${n} =  add pointy note  css=dl#plone-contentmenu-factories dd.actionMenuContent
    ...    note the add new menu no longer includes folder or collection
    ...    position=left
    add new page
    with the label  Title  input text  Menus
    with the label  Summary  input text  "only fools and chips" takeaway menu
    visual edit "We strive to make the best fish and chips your unemployment benefit can buy"
    #uploads a pic the shop.
    click button  Save

    #(note the pic goes into the page and the page appears as "menu" in the top nav.
    # Note also display menu is gone)

    narrate "Now he needs to add his menu items"
    click add new
    add new page
    with the label  Title  Fish
    with the label  Summary  Cod dipped in fat
    narrate "We just added a page within a page"
    narrate "No fiddling with Folders or default page display settings"

    enters fish description and uploads image of his fish (note fish image isn't appearing in side nav as its inside fish page)
    goes back to menu page
    Now we wants to list his menu. He clicks edit, adds "The chippie menu" sub title and then clicks "add tile" button.
    he selects listingtile. (note by default its query already shows folder contents so no need to change). He selects summary view. Hits create.
    In the editor he sees a shortcode and a preview of what the listing will look like (hopefully)
    he clicks save and views the page which includes the fish, description and thumbnail of the fish image
    now he wants to extend his menu. he adds new page called "chips".
    enters chips description and uploads pic of chips.
    clicks back up to "menu" page and shows that chips automatically got added to the menu listing



*** Keywords ***

click add new
    Click link  css=dl#plone-contentmenu-factories dt.actionMenuHeader a

add new page
    Click link  css=a#document


visual edit "${text}"
    select frame  id=text_ifr
    Input text  id=content  ${text}
    unselect frame
    # see http://stackoverflow.com/questions/17306305/how-to-select-the-text-of-a-tinymce-field-with-robot-framework-and-selenium2libr

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
  element should be visible  css=.mceLayout .mceToolbar
  Click link  css=.mce_plonetiles
  page should contain  Dummy tile
  select frame  css=.plonepopup iframe
#  element should be visible  css=form#add-tile
  with the label  Dummy tile  select checkbox
  click button  Create
#  page should contain  img
#  element should be visible css=img.mceTile
  click button  Save
  # still editing in tinymce
  click button  Save


# Then

A visitor can view "${text}"
  wait until page contains  ${text}
#  Log out
#  Go to  ${PLONE_URL}/a-document
#  Page should contain  Test tile rendered




With the label
    [arguments]     ${title}   ${extra_keyword}   @{list}
    ${for}=  Get Element Attribute  xpath=//label[contains(., "${title}")]@for
    Run Keyword     ${extra_keyword}  id=${for}   @{list}