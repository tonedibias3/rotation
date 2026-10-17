# Headless browser test: python3 scripts/e2e.py (needs playwright + chromium at /opt/pw-browsers/chromium). Screenshots go to a temp dir.
import json, os, time
from playwright.sync_api import sync_playwright
URL='file://'+os.path.abspath(os.path.join(os.path.dirname(__file__),'..','app','index.html'))
import tempfile; out=tempfile.mkdtemp(); res=[]
def ok(n,c,e=''): res.append(('PASS' if c else 'FAIL',n,e))
def boot(b,settings='{"splash":false}'):
    ctx=b.new_context(viewport={'width':390,'height':844},accept_downloads=True,service_workers='block')
    pg=ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/*',lambda r: r.abort() if r.request.url.startswith('http') else r.continue_())
    pg.goto(URL); pg.evaluate(f"localStorage.setItem('rotation.settings','{settings}')"); pg.reload(); pg.wait_for_timeout(1500)
    return pg,errs
def txt(pg): return pg.inner_text('#view').lower()
now=int(time.time()*1000)
def mk(n): return {'app':'rotation','v':2,'items':[{'id':f'i{k:02d}','name':f'Piece {k}','brand':'','category':'tops','color':'black','photo':'','createdAt':now} for k in range(n)],'days':{},'looks':[],'settings':{}}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    pg,errs=boot(b)
    ok('empty closet shows Start your closet','start your closet' in txt(pg))
    ok('no get-started duplicate on empty closet','get started' not in txt(pg))
    pg.click('[data-act=seed]'); pg.wait_for_timeout(1200)
    ok('get-started panel after starter list','get started' in txt(pg) and 'add 5 pieces' in txt(pg))
    pg.screenshot(path=out+'/closet.png')
    pg.click('#pill [data-tab=log]'); pg.wait_for_timeout(600)
    ok('Get started also on Log','get started' in txt(pg))
    ok('Share this fit button on Log',pg.locator('button:has-text("Share this fit")').count()==1)
    pg.locator('button:has-text("Share this fit")').click(); pg.wait_for_timeout(400)
    ok('share with nothing picked: no sheet',pg.locator('#sh-go').count()==0)
    pg.locator('[data-act=pick]').first.click(); pg.wait_for_timeout(500)
    pg.locator('button:has-text("Share this fit")').click(); pg.wait_for_timeout(2000)
    ok('share sheet opens after picking a piece',pg.locator('#sh-go').count()==1)
    pg.screenshot(path=out+'/share.png')
    pg.click('[data-act=share-close]'); pg.wait_for_timeout(300)
    ok('step 2 done after logging',pg.locator('.gs-r.done').count()>=1)
    pg.click('[data-act=tab][data-tab=settings]'); pg.wait_for_timeout(500)
    href=pg.locator('a:has-text("Send feedback")').get_attribute('href')
    ok('feedback mailto to hello@rotation.fit',href.startswith('mailto:hello@rotation.fit?subject=Rotation%20feedback'))
    ok('feedback body carries counts only, not item names','Jordan' not in href and 'Levi' not in href)
    pg.screenshot(path=out+'/settings.png',full_page=False)
    # import crafted 9-item backup -> nudge
    pf=out+'/in9.json'; json.dump(mk(9),open(pf,'w'))
    pg.set_input_files('#f-import',pf); pg.wait_for_timeout(1500)
    pg.click('[data-act=tab][data-tab=closet]') if pg.locator('[data-act=tab][data-tab=closet]').count() else None
    pg.wait_for_timeout(600)
    pg.evaluate("document.querySelector('#pill [data-tab=closet]').click()"); pg.wait_for_timeout(600)
    ok('backup nudge shows with 9+ items, never backed up','back up your closet' in txt(pg))
    pg.screenshot(path=out+'/nudge.png')
    with pg.expect_download() as d: pg.click('[data-act=export]')
    bk=out+'/bk.json'; d.value.save_as(bk); j=json.load(open(bk)); pg.wait_for_timeout(500)
    ok('export file valid and complete',j['app']=='rotation' and len(j['items'])>=9,str(len(j['items'])))
    ok('nudge gone after export','back up your closet' not in txt(pg))
    ok('lastBackup saved',pg.evaluate("JSON.parse(localStorage.getItem('rotation.settings')).lastBackup")>0)
    pg.evaluate("(()=>{const s=JSON.parse(localStorage.getItem('rotation.settings'));s.lastBackup=Date.now()-20*864e5;localStorage.setItem('rotation.settings',JSON.stringify(s))})()")
    ok('no page errors (device 1)',not errs,'; '.join(errs)[:200])
    # fresh device import round trip
    pg2,errs2=boot(b)
    pg2.click('[data-act=tab][data-tab=settings]') if pg2.locator('[data-act=tab][data-tab=settings]').count() else None
    pg2.wait_for_timeout(400)
    pg2.set_input_files('#f-import',bk); pg2.wait_for_timeout(1500)
    pg2.evaluate("document.querySelector('#pill [data-tab=closet]').click()"); pg2.wait_for_timeout(500)
    n=pg2.locator('.card[data-id]').count()
    ok('round trip: fresh device restores every piece',n==len(j['items']),f'{n} cards vs {len(j["items"])} items')
    # reload persistence + hide
    pg2.reload(); pg2.wait_for_timeout(1500)
    ok('data survives reload',pg2.locator('.card[data-id]').count()==len(j['items']))
    ok('Get started present before hide','get started' in txt(pg2))
    pg2.click('[data-act=gs-hide]'); pg2.wait_for_timeout(300)
    ok('Hide removes panel','get started' not in txt(pg2))
    pg2.reload(); pg2.wait_for_timeout(1500)
    ok('Hide persists after reload','get started' not in txt(pg2))
    ok('no page errors (device 2)',not errs2,'; '.join(errs2)[:200])
    # quick add: fresh device, 3 generated photos
    import zlib, struct
    def png(w,h,rgb):
        raw=b''.join(b'\x00'+bytes(rgb)*w for _ in range(h))
        def ch(t,d): c=struct.pack('>I',len(d))+t+d; return c+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
        return b'\x89PNG\r\n\x1a\n'+ch(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))+ch(b'IDAT',zlib.compress(raw))+ch(b'IEND',b'')
    pg4,errs4=boot(b)
    ok('empty state offers Add from photos','add from photos' in txt(pg4))
    files=[{'name':f'p{i}.png','mimeType':'image/png','buffer':png(300+i*40,200,(200,40*i,90))} for i in range(3)]
    pg4.set_input_files('#f-qa',files); pg4.wait_for_timeout(2500)
    ok('quick add sheet opens with 3 rows',pg4.locator('.qa-r').count()==3)
    pg4.locator('[data-act=qa-cat][data-v=shoes]').click(); pg4.wait_for_timeout(200)
    pg4.locator('input[data-qn="0"]').fill('Union Jordan 4')
    pg4.locator('[data-act=qa-cat][data-v=shoes]').click(); pg4.wait_for_timeout(200)
    ok('typed name survives re-render',pg4.locator('input[data-qn="0"]').input_value()=='Union Jordan 4')
    pg4.screenshot(path=out+'/quickadd.png')
    pg4.click('#qa-save'); pg4.wait_for_timeout(1500)
    ok('3 pieces saved with photos',pg4.locator('.card[data-id] img').count()>=3,str(pg4.locator('.card[data-id]').count()))
    pg4.reload(); pg4.wait_for_timeout(1500)
    t4=txt(pg4)
    ok('named + auto-named pieces persist','union jordan 4' in t4 and 'shoe 2' in t4)
    ok('no search UI left in settings','photo search' not in pg4.evaluate("document.body.innerText.toLowerCase()") )
    ok('no page errors (quick add)',not errs4,'; '.join(errs4)[:200])
    # regression: adding a piece from Log keeps scroll position; month recap button opens the share sheet
    pg5,errs5=boot(b)
    big=mk(40)
    for k,it in enumerate(big['items']): it['category']='shoes' if k%2 else 'tops'
    pf5=out+'/in40.json'; json.dump(big,open(pf5,'w'))
    pg5.click('[data-act=tab][data-tab=settings]') if pg5.locator('[data-act=tab][data-tab=settings]').count() else pg5.evaluate("document.querySelector('[data-act=tab][data-tab=settings]').click()")
    pg5.wait_for_timeout(400)
    pg5.set_input_files('#f-import',pf5); pg5.wait_for_timeout(1500)
    pg5.evaluate("document.querySelector('#pill [data-tab=log]').click()"); pg5.wait_for_timeout(600)
    pg5.locator('[data-act=pick]').first.click(); pg5.wait_for_timeout(400)
    pg5.evaluate("window.scrollTo(0,document.body.scrollHeight)"); pg5.wait_for_timeout(300)
    y0=pg5.evaluate("window.scrollY")
    pg5.evaluate("document.querySelector('[data-act=new-item]').click()"); pg5.wait_for_timeout(500)
    pg5.locator('#f-name').fill('Test shoe'); pg5.locator('#b-save').click(); pg5.wait_for_timeout(1200)
    y1=pg5.evaluate("window.scrollY")
    ok('adding a piece from Log keeps scroll position',y0>200 and abs(y1-y0)<80,f'{y0} -> {y1}')
    pg5.evaluate("document.querySelector('#pill [data-tab=calendar]').click()"); pg5.wait_for_timeout(500)
    pg5.evaluate("document.querySelector('[data-act=tab][data-tab=stats]').click()"); pg5.wait_for_timeout(600)
    pg5.evaluate("document.querySelector('[data-act=recap-open]').click()"); pg5.wait_for_timeout(2000)
    ok('month recap button opens the share sheet',pg5.locator('#sh-go').count()==1)
    ok('no page errors (scroll + recap)',not errs5,'; '.join(errs5)[:200])

    # backup round trip with days, extra outfits, ratings, looks, favorites and settings (reads what is persisted, not app internals)
    rich={'app':'rotation','v':2,
     'items':[
      {'id':'i00','name':'Black tee','brand':'Supreme','category':'tops','color':'black','photo':'','createdAt':now,'fav':True,'price':48,'sub':'T-shirt'},
      {'id':'i01','name':'Wide jeans','brand':'Levi','category':'bottoms','color':'blue','photo':'','createdAt':now},
      {'id':'i02','name':'Gym shorts','brand':'Nike','category':'bottoms','color':'grey','photo':'','createdAt':now},
      {'id':'i03','name':'Jordan 4','brand':'Nike','category':'shoes','color':'green','photo':'','createdAt':now,'fav':True},
      {'id':'i04','name':'Cap','brand':'New Era','category':'accessories','color':'navy','photo':'','createdAt':now},
      {'id':'i05','name':'Bleu','brand':'Chanel','category':'scents','color':'','photo':'','createdAt':now,'sub':'Woody'}],
     'days':{
      '2026-10-10':{'items':['i00','i01'],'tag':'work','rating':4,'scent':'i05','scentRating':3.5,'shoe':'i03','when':'morning,afternoon','note':'long day','place':'Augusta',
        'more':[{'items':['i02'],'tag':'casual','when':'evening','rating':2.5}],
        'plans':[{'items':['i04'],'tag':'mixed'}]},
      '2026-10-11':{'scent':'i05','scentRating':5}},
     'looks':[{'id':'l1','name':'Friday','items':['i00','i01','i03']},{'id':'l2','name':'Gym','items':['i02']}],
     'settings':{'sort':'worn','accent':'ember','cview':'swipe','order':['shoes','tops'],'occ':[{'id':'o1','label':'Gym'}],'subs':{'tops':['Crewneck']}}}
    rf=out+'/rich.json'; json.dump(rich,open(rf,'w'))
    alt=json.loads(json.dumps(rich)); alt['days']['2026-10-10']['rating']=1; alt['days']['2026-10-10']['note']='phone version'; del alt['days']['2026-10-11']; alt['looks']=alt['looks'][:1]
    af=out+'/alt.json'; json.dump(alt,open(af,'w'))
    SNAP="""async()=>{const db=await new Promise((res,rej)=>{const r=indexedDB.open('rotation',1);r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error)});
      const g=k=>new Promise(res=>{const q=db.transaction('kv').objectStore('kv').get(k);q.onsuccess=()=>res(q.result)});
      return {items:(await g('items'))||[],days:(await g('days'))||{},looks:(await g('looks'))||[],set:JSON.parse(localStorage.getItem('rotation.settings')||'{}')}}"""
    def snap(pg): return pg.evaluate(SNAP)
    def chk(tag,sn):
        it={i['id']:i for i in sn['items']}
        ok(tag+': 6 pieces, favorites and extra fields kept',len(sn['items'])==6 and it['i00'].get('fav') is True and it['i03'].get('fav') is True and not it['i01'].get('fav') and it['i00'].get('price')==48 and it['i05'].get('sub')=='Woody',str(sn['items'])[:160])
        d=sn['days'].get('2026-10-10',{})
        ok(tag+': day outfit, tag, rating, shoe, scent, when kept',d.get('items')==['i00','i01'] and d.get('tag')=='work' and d.get('rating')==4 and d.get('shoe')=='i03' and d.get('scent')=='i05' and d.get('scentRating')==3.5 and d.get('when')=='morning,afternoon',str(d)[:200])
        ok(tag+': extra outfit and plan kept',len(d.get('more',[]))==1 and d['more'][0]['items']==['i02'] and d['more'][0]['rating']==2.5 and d['plans'][0]['items']==['i04'],str(d.get('more'))[:160])
        d11=sn['days'].get('2026-10-11',{})
        ok(tag+': scent-only day kept',d11.get('scent')=='i05' and d11.get('scentRating')==5,str(d11)[:120])
        ok(tag+': looks kept',[l['id'] for l in sn['looks']]==['l1','l2'] and sn['looks'][0]['items']==['i00','i01','i03'],str(sn['looks'])[:160])
        st=sn['set']
        ok(tag+': settings kept',st.get('sort')=='worn' and st.get('accent')=='ember' and st.get('cview')=='swipe' and st.get('order')==['shoes','tops'] and st['occ'][0]['label']=='Gym' and st['subs']['tops']==['Crewneck'],str(st)[:200])
    def to_settings(pg):
        pg.evaluate("(()=>{if(document.querySelector('#f-import'))return;const t=document.querySelector('[data-act=tab][data-tab=settings]');if(t)t.click()})()"); pg.wait_for_timeout(400)
    pg6,errs6=boot(b)
    to_settings(pg6)
    pg6.set_input_files('#f-import',rf); pg6.wait_for_timeout(1800)
    chk('import',snap(pg6))
    pg6.reload(); pg6.wait_for_timeout(1500)
    chk('after reload',snap(pg6))
    to_settings(pg6)
    with pg6.expect_download() as d6: pg6.evaluate("document.querySelector('[data-act=export]').click()")
    bk6=out+'/bk6.json'; d6.value.save_as(bk6); j6=json.load(open(bk6))
    ok('export keeps days and looks',len(j6['looks'])==2 and j6['days']['2026-10-10']['rating']==4 and j6['days']['2026-10-10']['more'][0]['items']==['i02'] and j6['days']['2026-10-11']['scentRating']==5)
    # second fresh device restores from the re-exported file
    pg7,errs7=boot(b)
    to_settings(pg7)
    pg7.set_input_files('#f-import',bk6); pg7.wait_for_timeout(1800)
    chk('export -> import on 2nd device',snap(pg7))
    # importing the same file again changes nothing and shows no conflict dialog
    to_settings(pg7)
    pg7.set_input_files('#f-import',bk6); pg7.wait_for_timeout(1200)
    sn=snap(pg7)
    ok('re-import is idempotent (no duplicates, no dialog)',len(sn['items'])==6 and len(sn['looks'])==2 and pg7.locator('#ask').count()==0)
    # conflict handling on a third device whose phone copy of a day differs from the backup
    def conflict_device():
        pg,er=boot(b); to_settings(pg)
        pg.set_input_files('#f-import',af); pg.wait_for_timeout(1800)
        pg.set_input_files('#f-import',rf); pg.wait_for_timeout(1200)
        return pg,er
    pg8,errs8=conflict_device()
    ok('conflict dialog appears when a day differs',pg8.locator('#ask').count()==1)
    pg8.locator('#ask [data-i="0"]').click(); pg8.wait_for_timeout(1500)
    ok('keep phone: day keeps the phone version',snap(pg8)['days']['2026-10-10']['rating']==1 and snap(pg8)['days']['2026-10-10']['note']=='phone version')
    ok('keep phone: new days and looks from backup still added','2026-10-11' in snap(pg8)['days'] and len(snap(pg8)['looks'])==2)
    pg9,errs9=conflict_device()
    pg9.locator('#ask [data-i="1"]').click(); pg9.wait_for_timeout(1500)
    ok('use backup: day takes the backup version',snap(pg9)['days']['2026-10-10']['rating']==4 and snap(pg9)['days']['2026-10-10']['note']=='long day')
    pg10,errs10=conflict_device()
    pg10.locator('#ask [data-i="2"]').click(); pg10.wait_for_timeout(1000)
    sn10=snap(pg10)
    ok('cancel: day unchanged and nothing from the backup added',sn10['days']['2026-10-10']['rating']==1 and '2026-10-11' not in sn10['days'] and len(sn10['looks'])==1)
    # a file that is not a backup is refused and changes nothing
    bad=out+'/bad.json'; open(bad,'w').write('{"hello":"world"}')
    n_before=len(snap(pg7)['items'])
    pg7.set_input_files('#f-import',bad); pg7.wait_for_timeout(800)
    ok('non-backup file refused with a clear message','not a rotation backup' in pg7.evaluate("document.body.innerText.toLowerCase()") and len(snap(pg7)['items'])==n_before)
    allerrs=errs6+errs7+errs8+errs9+errs10
    ok('no page errors (backup round trip)',not allerrs,'; '.join(allerrs)[:200])

    # interactions: tap a piece = view, press and hold = edit (Closet); Log keeps tap = select, hold = edit
    pg11,errs11=boot(b)
    to_settings(pg11)
    pg11.set_input_files('#f-import',rf); pg11.wait_for_timeout(1800)
    pg11.evaluate("document.querySelector('#pill [data-tab=closet]').click()"); pg11.wait_for_timeout(700)
    def hold(pg,sel,ms=650):
        pg.locator(sel).first.scroll_into_view_if_needed(); pg.wait_for_timeout(250)
        bx=pg.locator(sel).first.bounding_box()
        pg.mouse.move(bx['x']+bx['width']/2,bx['y']+bx['height']/2); pg.mouse.down(); pg.wait_for_timeout(ms); pg.mouse.up(); pg.wait_for_timeout(500)
    ok('closet hint says tap to view, hold to edit','tap a piece to view it' in txt(pg11) and 'press and hold to edit it' in txt(pg11))
    pg11.locator('.card[data-id="i00"]').first.click(); pg11.wait_for_timeout(500)
    ok('closet tap opens the view sheet (Edit button, no form)',pg11.locator('#sheet [data-act=view-edit]').count()==1 and pg11.locator('#f-name').count()==0)
    pg11.locator('#sheet [data-act=view-edit]').click(); pg11.wait_for_timeout(500)
    ok('Edit button on the view opens the edit form',pg11.locator('#f-name').count()==1 and pg11.locator('#f-name').input_value()=='Black tee')
    pg11.evaluate("(()=>{const c=document.querySelector('[data-act=sheet-close]');if(c)c.click()})()"); pg11.wait_for_timeout(500)
    ok('edit form closed',pg11.locator('#f-name').count()==0)
    hold(pg11,'.card[data-id="i01"]')
    ok('closet press and hold opens the edit form',pg11.locator('#f-name').count()==1 and pg11.locator('#f-name').input_value()=='Wide jeans' and pg11.locator('#sheet [data-act=view-edit]').count()==0)
    pg11.evaluate("document.querySelector('[data-act=sheet-close]').click()"); pg11.wait_for_timeout(500)
    ok('after a hold, the release does not also open the view',pg11.locator('#sheet [data-act=view-edit]').count()==0 and pg11.locator('#f-name').count()==0)
    # Log picker
    pg11.evaluate("document.querySelector('#pill [data-tab=log]').click()"); pg11.wait_for_timeout(700)
    ok('log hint says hold to edit','press and hold a piece to edit it' in txt(pg11))
    pg11.locator('.card[data-act=pick][data-id="i02"]').first.click(); pg11.wait_for_timeout(400)
    ok('log tap still selects a piece',pg11.locator('.card[data-act=pick][data-id="i02"]').first.get_attribute('aria-pressed')=='true')
    hold(pg11,'.card[data-act=pick][data-id="i04"]')
    ok('log press and hold opens edit and does not select',pg11.locator('#f-name').count()==1 and pg11.locator('#f-name').input_value()=='Cap')
    pg11.evaluate("document.querySelector('[data-act=sheet-close]').click()"); pg11.wait_for_timeout(500)
    ok('log selection unchanged after hold-to-edit',pg11.locator('.card[data-act=pick][data-id="i04"]').first.get_attribute('aria-pressed')=='false' and pg11.locator('.card[data-act=pick][data-id="i02"]').first.get_attribute('aria-pressed')=='true')
    ok('no page errors (tap/hold interactions)',not errs11,'; '.join(errs11)[:200])

    # regression: Escape closes the view sheet and the edit form (it threw "FD is not defined" before)
    pg12,errs12=boot(b)
    to_settings(pg12)
    pg12.set_input_files('#f-import',rf); pg12.wait_for_timeout(1800)
    pg12.evaluate("document.querySelector('#pill [data-tab=closet]').click()"); pg12.wait_for_timeout(700)
    pg12.locator('.card[data-id="i00"]').first.click(); pg12.wait_for_timeout(400)
    pg12.keyboard.press('Escape'); pg12.wait_for_timeout(400)
    ok('Escape closes the view sheet',pg12.locator('#sheet [data-act=view-edit]').count()==0)
    hold(pg12,'.card[data-id="i01"]')
    pg12.keyboard.press('Escape'); pg12.wait_for_timeout(400)
    ok('Escape closes the edit form',pg12.locator('#f-name').count()==0)
    ok('no page errors on Escape',not errs12,'; '.join(errs12)[:200])

    # regression: adding a piece from its view sheet keeps the screen where it was (no jump to the top, no tab change)
    pg13,errs13=boot(b)
    big13=mk(40)
    for k,it in enumerate(big13['items']): it['category']='shoes' if k%2 else 'tops'
    pf13=out+'/in40b.json'; json.dump(big13,open(pf13,'w'))
    to_settings(pg13)
    pg13.set_input_files('#f-import',pf13); pg13.wait_for_timeout(1800)
    pg13.evaluate("document.querySelector('#pill [data-tab=closet]').click()"); pg13.wait_for_timeout(700)
    pg13.evaluate("window.scrollTo(0,document.body.scrollHeight)"); pg13.wait_for_timeout(300)
    pg13.evaluate("window.scrollBy(0,-500)"); pg13.wait_for_timeout(300)
    y0=pg13.evaluate("window.scrollY")
    vis=pg13.evaluate("(()=>{const l=[...document.querySelectorAll('.card[data-id]')].filter(c=>{const r=c.getBoundingClientRect();return r.top>120&&r.bottom<700&&r.left>=0&&r.right<=390});return l.slice(0,2).map(c=>c.dataset.id)})()")
    ok('found pieces on screen far down the closet',y0>300 and len(vis)>=2,f'y0={y0} vis={vis}')
    for n,cid in enumerate(vis[:2]):
        try:
            pg13.locator(f'.card[data-id="{cid}"]').first.click(timeout=4000); pg13.wait_for_timeout(450)
            pg13.locator('#sheet [data-act=view-wear]').click(timeout=4000); pg13.wait_for_timeout(900)
        except Exception as e:
            ok(f'add #{n+1} from the view sheet: could open view and add',False,str(e).split('\n')[0][:120]); break
        y1=pg13.evaluate("window.scrollY")
        ok(f'add #{n+1} from the view sheet: page stays put',abs(y1-y0)<=40,f'{y0} -> {y1}')
        ok(f'add #{n+1}: still on the Closet tab',pg13.evaluate("document.querySelector('#pill [data-tab=closet]').getAttribute('aria-current')")=='page')
        ok(f'add #{n+1}: view sheet closed and confirmation shown',pg13.locator('#sheet [data-act=view-wear]').count()==0 and 'added to today' in pg13.inner_text('#toast').lower())
    tk=pg13.evaluate("(()=>{const d=new Date(),p=n=>String(n).padStart(2,'0');return d.getFullYear()+'-'+p(d.getMonth()+1)+'-'+p(d.getDate())})()")
    pg13.wait_for_timeout(1500)
    dd=pg13.evaluate("""async(k)=>{const db=await new Promise((res,rej)=>{const r=indexedDB.open('rotation',1);r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error)});
      const v=await new Promise(res=>{const q=db.transaction('kv').objectStore('kv').get('days');q.onsuccess=()=>res(q.result)});return v&&v[k]?v[k].items:[]}""",tk)
    ok('both pieces saved to today\'s outfit',sorted(dd)==sorted(vis[:2]),str(dd))
    ok('no page errors (add from view)',not errs13,'; '.join(errs13)[:200])
    b.close()
w=max(len(r[1]) for r in res)
for r in res: print(r[0],'|',r[1].ljust(w),'|',r[2])
print(sum(r[0]=='PASS' for r in res),'/',len(res))
