library(shiny)
library(shinydashboard)
library(DT)
library(shinyjs)
library(sodium)
library(stringr)
library(RMySQL)

#If connection reaches limit
#dbDisconnect(con)

#First run
#con = dbConnect(RMySQL::MySQL(), dbname = "data_base",username = "root", password = "f129968890", host = "localhost", port = 3306)




# Main login screen
loginpage <- div(id = "loginpage", style = "width: 500px; max-width: 100%; margin: 0 auto; padding: 20px;",
                 wellPanel(
                   tags$h2("登入", class = "text-center", style = "padding-top: 0;color:#333; font-weight:600;"),
                   textInput("userName", placeholder="帳號", label = tagList(icon("user"), "帳號")),
                   passwordInput("passwd", placeholder="密碼", label = tagList(icon("unlock-alt"), "密碼")),
                   br(),
                   div(
                     style = "text-align: center;",
                     actionButton("login", "登入", style = "color: white; background-color:red;
                                  padding: 10px 15px; width: 150px; cursor: pointer;
                                  font-size: 18px; font-weight: 600;"),
                     shinyjs::hidden(
                       div(id = "nomatch",
                           tags$p("很抱歉，密碼或帳號錯誤!",
                                  style = "color: red; font-weight: 600; 
                                  padding-top: 5px;font-size:16px;", 
                                  class = "text-center"))),
                     br(),
                     br(),
                     tags$code("帳號: myuser  密碼: mypass"),
                     br(),
                     tags$code("帳號: myuser1  密碼: mypass1")
                     ))
                     )

credentials = data.frame(
  username_id = c("myuser", "myuser1"),
  passod   = sapply(c("mypass", "mypass1"),password_store),
  permission  = c("basic", "advanced"), 
  stringsAsFactors = F
)

header <- dashboardHeader( title = "系隊⼈⼒資源系統", uiOutput("logoutbtn"))

sidebar <- dashboardSidebar(uiOutput("sidebarpanel")) 
body <- dashboardBody(shinyjs::useShinyjs(), uiOutput("body"))
ui<-dashboardPage(header, sidebar, body, skin = "red")

server <- function(input, output, session) {
  
  login = FALSE
  USER <- reactiveValues(login = login)
  
  observe({ 
    if (USER$login == FALSE) {
      if (!is.null(input$login)) {
        if (input$login > 0) {
          Username <- isolate(input$userName)
          Password <- isolate(input$passwd)
          if(length(which(credentials$username_id==Username))==1) { 
            pasmatch  <- credentials["passod"][which(credentials$username_id==Username),]
            pasverify <- password_verify(pasmatch, Password)
            if(pasverify) {
              USER$login <- TRUE
            } else {
              shinyjs::toggle(id = "nomatch", anim = TRUE, time = 1, animType = "fade")
              shinyjs::delay(3000, shinyjs::toggle(id = "nomatch", anim = TRUE, time = 1, animType = "fade"))
            }
          } else {
            shinyjs::toggle(id = "nomatch", anim = TRUE, time = 1, animType = "fade")
            shinyjs::delay(3000, shinyjs::toggle(id = "nomatch", anim = TRUE, time = 1, animType = "fade"))
          }
        } 
      }
    }    
  })
  
  output$logoutbtn <- renderUI({
    req(USER$login)
    tags$li(a(icon("fa fa-sign-out"), "登出", 
              href="javascript:window.location.reload(true)"),
            class = "dropdown", 
            style = "background-color: #eee !important; border: 0;
            font-weight: bold; margin:5px; padding: 10px;")
  })
  
  output$sidebarpanel <- renderUI({
    if (USER$login == TRUE ){ 
      sidebarMenu(
        menuItem("Main Page", tabName = "dashboard", icon = icon("dashboard"))
      )
    }
  })
  
  output$body <- renderUI({
    if (USER$login == TRUE ) {
      tabItem(tabName ="dashboard", class = "active",
              fluidRow(
                box(width = 12, dataTableOutput('results'))
              ))
      fluidPage(
        title = "Examples of DataTables",
        sidebarLayout(
          if(1<0){sidebarPanel(
            conditionalPanel(
              'input.dataset === "dbReadTable(con, "song")"',
              checkboxGroupInput("show_vars", "Columns in song to show:",
                                 names(dbReadTable(con, "song")), selected = names(dbReadTable(con, "song")))
            ),
            conditionalPanel(
              'input.dataset === "datatable(dbReadTable(con, "albums")"',
              helpText("Click the column header to sort a column.")
            ),
            conditionalPanel(
              'input.dataset === "datatable(dbReadTable(con, "boards")"',
              helpText("Display 5 records by default.")
            ) 
          )},
          mainPanel(
            tabsetPanel(
              id = 'dataset',
              tabPanel("尋找球員", DT::dataTableOutput("mytable2"),
                       textInput("sname", "輸入球員姓名:", "球員姓名"),
                       actionButton("find", "搜尋")),
              tabPanel("顯示所有球員", DT::dataTableOutput("mytable3"),
#                       textInput"pnam", "Enter playlist name:", "list name"),
#                       textInput("uid", "Enter uid:", "uid"),
                       actionButton("inl", "顯示")),
              tabPanel("建立練球時段", DT::dataTableOutput("mytable4"),
                       textInput("tim", "輸入練球時間:", "時間"),
                       textInput("cou", "輸入練球場地:", "地點"),
#                       numericInput("sid", "Enter Singer ID:", "SID"),
#                       numericInput("aid", "Enter Album ID:", "AID"),
                       actionButton("ins", "建立")),
              tabPanel("尋找系隊", DT::dataTableOutput("mytable5"),
                       textInput("x", "輸入運動:", "運動名稱"),
                       actionButton("go", "搜尋")),
              tabPanel("查看練球狀況", DT::dataTableOutput("mytable1"),
#                       textInput("pi", "Enter playlist ID:", "ID"),
#                       textInput("id", "Enter song ID:", "ID"),
                       actionButton("inse", "顯示"))
            )

            
          )
        )
      )
      
      

      
      
      
    }
    else {
      loginpage
    }
    
    
    
    
    
  })
  

    
  # "select name from song where AID = (select AID from albums where Aname = 'Suck')"

  
  show_training <- eventReactive(input$inse, {
    show_training_session(input$pi, input$id)
  })
  
  show_training_session <- function(a, b){
    return(trainings)
  }
  
  
  output$mytable1 <- DT::renderDataTable({
    DT::datatable(show_training(), options = list(orderClasses = TRUE))
  })
  
  
  find_player <- eventReactive(input$find, {
    find_ID(input$sname)
  })
  
  find_ID <- function(playerName){
    return(players %>% filter(name == playerName))
  }
  
  # sorted columns are colored now because CSS are attached to them
  output$mytable2 <- DT::renderDataTable({
    DT::datatable(find_player(), options = list(orderClasses = TRUE))
  })
  
  showPlayerList <- eventReactive(input$inl, {
    show_player(input$pnam, input$uid)
  })
  
  show_player <- function(a, b){
    return(players)
  }
  
  # customize the length drop-down menu; display 5 rows per page by default
  output$mytable3 <- DT::renderDataTable({
    DT::datatable(showPlayerList(), options = list(lengthMenu = c(5, 30, 50), pageLength = 5))
  })
  
  
  insertResult <- eventReactive(input$ins, {
    insert_training(input$tim, input$cou)
  })
  
  insert_training <- function(input_time, input_court){
    trainings <- rbind(trainings, c(input_time, input_court))
    return(trainings)
  }
  
  output$mytable4 <- DT::renderDataTable({
    DT::datatable(insertResult(), options = list(lengthMenu = c(5, 30, 50), pageLength = 5))
  })
  
  searchResult <- eventReactive(input$go, {
    select_team(input$x)
  })
  
  select_team <- function(teamName){
    return(team %>% filter(sport == teamName))
  }
  
  output$mytable5 <- DT::renderDataTable({
    DT::datatable( searchResult() , options = list(lengthMenu = c(5, 30, 50), pageLength = 5))
  })
  
  


  
}




runApp(list(ui = ui, server = server), launch.browser = TRUE)

