*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/speak.robot
Resource  Selenium2Screenshots/keywords.robot
Library   collective.tinymcetiles.tests.test_acceptance.Keywords

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***
${SLEEP}  0.4
# to speed up: bin/robot -t "Del Boy opens a chippie using tiles" -v SLEEP:0

${CHIP_PIC}  http://3.bp.blogspot.com/-u1HS4kzoGuM/UfNzwLcl0BI/AAAAAAAAG0w/otZtiEHx72w/s1600/DSC_7515.jpg
${FISH_PIC}  http://www.messersmith.name/wordpress/wp-content/uploads/2009/11/titan_triggerfish_balistoides_viridescens_P7290834.jpg
${SHOP_PIC}  http://images.smh.com.au/2012/01/20/2905552/MJtravelwide6_20120120132625161061-420x0.jpg


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
    Given a site owner
    narrate "Now he can put is food menu online in no time!"
    click link  Home
    Click "Add New"
    show pointy note on "Add New > Page" "First he creates a new page"
    Click "Add New > Page"
    with the label  Title  input text  Menus
    with the label  Summary  input text  "only fools and chips" takeaway menu
    show pointy note on "Visual Editor" "Content still works the same way"
    visual edit "We strive to make the best fish and chips your unemployment benefit can buy"
    Save Page
    Click Link  Edit
    upload image   ${SHOP_PIC}
    Save Page

    # TODO: need to ensure images are stored inside pages and can't see objects
    page should not contain  jpg
    show pointy note on "Content Image" "The image we just uploaded..."
    Click link  Contents
    show pointy note on "Contents Item" "...is stored in the page"
    show pointy note on "Breadcrumbs" "so no need to create a folder"
    Click "Add New"
    show pointy note on "Add New dropdown" "in fact we no longer have folder or collection types"

    narrate "Now he needs to add his menu items"

    show pointy note on "Add New > Page" "Adding a page now adds a sub-page"
    Click "Add New > Page"
    with the label  Title  input text  Fish
    with the label  Summary  input text  Cod dipped in fat
    show pointy note on "Breadcrumbs" "No fiddling with Folders"
    show pointy note on "Breadcrumbs" "or default page display settings"
    Save Page
    Click Link  Edit
    upload image  ${FISH_PIC}
    Save Page
    show pointy note on "Add New dropdown" "there isn't even a display any anymore"
    #TODO need to get rid of the display menu

    click link  Menus
    narrate "Now we wants to list his menu"

    narrate "Del is lazy so he wants an automated the listing of his menu items"
    narrate "previous he'd have to use collections and default pages which was both confusing and inflexible"
    click link  Edit
    show pointy note on "Insert tile button" "Instead we're going to use a 'tile'"
    Click Button Insert Tile
    #TODO insert a heading text, make into heading and then insert the tile after the heading

    Use Dialog "Add Tile"
    Show pointy note on "Tile Type > Content Listing" "Content listing tiles replaces collections"
    with the label  Content listing  select checkbox
    click button  Create
    Show pointy note on "Content Listing > Criteria" "by default we list current contents just like a folder view would have"
    #TODO we need to restrict it to pages so the shop image isn't listed
    Show pointy note on "Content Listing > Display Mode" "He can choose how he wants it displayed"
    Select "Content Listing > Display Mode" "Summary view"
    click button  Save
    unselect frame

    narrate "The tile is inserted as a shortcode"
    narrate "including a preview of what the listing will look like"
    #TODO need to switch to actual using shortcodes instead of image placeholders
    #TODO point to shortcode in editor and a preview of what the listing will look like (hopefully)
    #TODO make preview work with shortcodes

    click button  Save
    narrate "not only has he automated his menu, but with content above and below it, it's more flexible than using collections"
    #TODO need to insert text above and below to make the above true.
    page should contain  Cod dipped in fat
    #TODO make contentlisting tile include thumbnail?

    narrate "Now he wants to extend is menu by adding Chips"
    Click "Add New"
    Click "Add New > Page"
    with the label  Title  input text  Chips
    with the label  Summary  input text  Potato dipped in fat
    click button  Save
    click link    Edit
    upload image  ${CHIP_PIC}
    click button  Save
    click link  Menus

    narrate "Chips have automatically been added to the menu"
    page should contain  Potato dipped in fat
    #TODO point at chip item instead of just narrate



    #TODO should show reediting an existing tile

    #TODO should show manualy editing an existing tile, or just inserting a tile by hand

    #TODO show adding tile into a static text portlet to show how tiles can replace portlets
    # e.g. no more collection portlet, news portlet or upcoming events portlets



*** Keywords ***

Save Page
    click button  Save
#	Wait Until Page Contains  Item created


show pointy note on "Add New > Page" "${note}"
    show pointy note  css=a.contenttype-document  ${note}  left

show pointy note on "Add New dropdown" "${note}"
    show pointy note  css=dl#plone-contentmenu-factories dd.actionMenuContent
    ...    ${note}
    ...    left

show pointy note on "Breadcrumbs" "${note}"
    show pointy note  css=#portal-breadcrumbs
    ...    ${note}
    ...    bottom


show pointy note on "Insert tile button" "${note}"
    Page should contain element  css=.mce_plonetiles
    show pointy note  css=.mce_plonetiles
    ...   ${note}
    ...   top

show pointy note on "Menus" "${note}"
    show pointy note  css=#portaltab-menus
    ...   ${note}
    ...   top

show pointy note on "Visual Editor" "${note}"
    show pointy note  css=#formfield-form-widgets-text
    ...   ${note}
    ...   top

show pointy note on "Contents Item" "${note}"
    show pointy note  css=.draggable
    ...   ${note}
    ...   top

show pointy note on "Content Image" "${note}"
    show pointy note  css=#content img
    ...   ${note}
    ...   top

Click Button Insert Tile
    Click Link  css=.mce_plonetiles

Use Dialog "Add Tile"
    select frame  css=.plonepopup iframe

Show pointy note on "Tile Type > Content Listing" "${note}"
    ${n}=  label "Content listing"
    show pointy note  ${n}  ${note}
    ...   top

Show pointy note on "Content Listing > Criteria" "${note}"
    element should be visible  css=.criteria
    show pointy note  css=.criteria
    ...     ${note}
    ...     top

Show pointy note on "Content Listing > Display Mode" "${note}"
    ${n}=  label "Display mode"
    show pointy note  ${n}
    ...  ${note}
    ...  top

Select "Content Listing > Display Mode" "${value}"
    ${n}=  label "Display mode"
#    scroll Component To View  ${n}
    select from list by label  ${n}  ${value}

show pointy note
    [arguments]     ${locator}  ${note}  ${position}
    Update element style  ${locator}  outline  3px dotted red
    ${n} =  add pointy note  ${locator}
    ...    ${note}
    ...    position=${position}
    ...   width=300  background=rgba(200,200,200,1)  border=3px solid black
    Update element style  ${n}  font  15px arial,sans-serif
    Update element style  ${n}  text-align  center
    Update element style  ${n}  border-radius  5px
    Update element style  ${n}  box-shadow  10px 10px 5px #888888
    Speak  ${note}
    wait for speech  ${note}  ${SLEEP}
    Remove element  ${n}
    Update element style  ${locator}  outline  0px


Narrate "${text}"
    #TODO: need to make this bigger, on nice grey transparent background
    ${note1} =  Add note  css=#content
    ...  ${text}
    ...   width=500  background=rgba(200,200,200,0.7)  position=bottom  border=3px solid black
    Update element style  ${note1}  font  25px arial,sans-serif
    Update element style  ${note1}  text-align  center
    Update element style  ${note1}  border-radius  15px
    Update element style  ${note1}  box-shadow  10px 10px 5px #888888

    #TODO: work out delay based on number of words
    Speak  ${text}
    wait for speech  ${text}  ${SLEEP}
    Remove element  ${note1}

Click "Add New"
    Click link  css=dl#plone-contentmenu-factories dt.actionMenuHeader a

Click "Add New > Page"
    Click link  css=a#document

visual edit "${text}"
    select frame  css=.mceIframeContainer iframe
    Input text  id=content  ${text}
    unselect frame
    # see http://stackoverflow.com/questions/17306305/how-to-select-the-text-of-a-tinymce-field-with-robot-framework-and-selenium2libr

upload image
    [arguments]     ${url}
    Page should contain element  css=.mce_image
    click link  css=.mce_image
    select frame  css=.plonepopup iframe
    # external images doesn't help our demo of showing containment
    #click link  External
    #input text  css=#imageurl  ${url}
    ${file}=  download file  ${url}
    click link  upload
    choose file  id=uploadfile  ${file}
    click button  Upload
    select from list by label  classes  Right
    select from list by label  dimensions  Mini (200x200)
    #sleep   1s
    Wait Until Keyword Succeeds  10s  0.5s  Element Should Be Enabled  css=input#insert-selection
    click button  OK
    unselect frame



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
  click button  Save
  unselect Frame
#  page should contain  img
#  element should be visible css=img.mceTile


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

