def SelectItem_2(driverHolder,name,item,by,CalismaSuresi,command,gecenZaman = 0,tekrarlamaAraligi = 1):
            
    result = None
    while driverHolder[1]==True and gecenZaman < CalismaSuresi:

        element = driverHolder[0].find_elements(by, item)
        if element:
            try:
                if command == "click":
                    element[0].click()
                    print(name,"Bulundu!")
                elif command == "text":
                    print(name,"Bulundu!")
                    if element[0].text is None:
                        print(name,"Aranıyor..." + str(CalismaSuresi - gecenZaman) +"   ",end="\r")
                        time.sleep(tekrarlamaAraligi)
                        gecenZaman = gecenZaman + tekrarlamaAraligi
                        continue

                    else:          
                        # print("returned : "+ element[0].text)        
                        return element[0].text
                elif command == "none":
                    if element[0] is None:
                        print(name,"Aranıyor..." + str(CalismaSuresi - gecenZaman) +"   ",end="\r")
                        time.sleep(tekrarlamaAraligi)
                        gecenZaman = gecenZaman + tekrarlamaAraligi
                        continue
                    else:
                        return element[0]
                else:
                    element[0].send_keys(command)
                    print(name,"Bulundu!")
                result = True
                break

            except Exception as e:
                EmptyArea = driverHolder[0].find_elements(By.TAG_NAME,"body")
                if EmptyArea:
                    print("boşlupa tıklandı")
                    EmptyArea[0].click()

                print("Hata alındı : "+name+"\n HATA...\n"+ str(e))
                print(name,"Aranıyor..." + str(CalismaSuresi - gecenZaman) +"   ",end="\r")
                time.sleep(tekrarlamaAraligi)
                gecenZaman = gecenZaman + tekrarlamaAraligi
                continue
                
        else:
            print(name,"Aranıyor..." + str(CalismaSuresi - gecenZaman) +"   ",end="\r")
            time.sleep(tekrarlamaAraligi)
            gecenZaman = gecenZaman + tekrarlamaAraligi
            continue
    if gecenZaman >= CalismaSuresi:
        result = False
    if result == False:
        print(name,"Bulunamadı !!!")
        driverHolder[1] = False
