**TestScript Template:**

<testcase>
    <scenario>
    
    <step>

         <name>
         
         <action>
         
         <target>
         
         <value>

         <screenshot_name>

         <sleep>

---------------------------------------------------------

testcase 1:
    scenario: <your test senario desc>
    
    step 1:
        name: input user user id >
        
        action: input | click | import | sleep | wait | validate | function | hover | goto | screenshot
        
        target: //input[@id="userid"]
        
        value: admin
        
        screenshot_name: testcase-1-2-3

        sleep: 10
        
    step 2:
        name: import some testcase
        
        action: import
        
        target: testcase 2  
  
    step 3:
        name: call custome function
        
        action: function
        
        target: function_name
        
        value: [,,,]  <params for the function>

testcase 2:
...
